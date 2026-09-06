from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import pytest

from soundsplit_knowledge.models import DIMENSIONS, PROFILE, KnowledgeError, SearchFilters
from soundsplit_knowledge.store import PostgresStore

ROOT = "11111111-1111-1111-1111-111111111111"
VECTOR = [1.0] + [0.0] * (DIMENSIONS - 1)


class Result:
    def __init__(self, *, one=None, rows=None):
        self.one = one
        self.rows = rows or []

    def fetchone(self):
        return self.one

    def fetchall(self):
        return self.rows


class Connection:
    def __init__(self, synced_at, rows=None):
        self.synced_at = synced_at
        self.rows = rows or []
        self.queries = []

    def execute(self, query, params=None):
        self.queries.append((query, params))
        if query.startswith("SET TRANSACTION"):
            return Result()
        if "FROM knowledge.sync_state" in query:
            return Result(one={"profile": PROFILE, "last_synced_at": self.synced_at,
                               "document_count": 49})
        return Result(rows=self.rows)


class Store(PostgresStore):
    def __init__(self, connection):
        super().__init__("postgresql://unused")
        self.fake = connection

    @contextmanager
    def connection(self, **_):
        yield self.fake


def test_stale_index_fails_closed_before_search():
    connection = Connection(datetime.now(timezone.utc) - timedelta(hours=25))

    with pytest.raises(KnowledgeError, match="stale"):
        Store(connection).search(ROOT, "query", VECTOR, SearchFilters(), max_age_hours=24)

    assert not any("WITH eligible" in query for query, _ in connection.queries)


def test_filters_are_parameterized_and_normative_policy_is_in_sql():
    connection = Connection(datetime.now(timezone.utc))
    filters = SearchFilters(ids=["adr-001"], tags=["sheet-music"],
                            accepted_decisions_only=True)

    result = Store(connection).search(ROOT, "ADR-001", VECTOR, filters)

    query, params = next(item for item in connection.queries if "WITH eligible" in item[0])
    assert "d.document_type='decision'" in query
    assert "lower(d.status)='accepted'" in query
    assert "c.knowledge_type='decision'" in query
    assert "ADR-001" not in query
    assert params["ids"] == ["ADR-001"]
    assert params["tags"] == ["sheet-music"]
    assert result["empty_reason"] == "no_matching_evidence"
