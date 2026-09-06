import json
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from importlib.resources import files

from .chunking import embedding_text
from .embeddings import validate_vectors
from .models import PROFILE, KnowledgeError, SearchFilters
from .notion import IDS, page_id


class PostgresStore:
    def __init__(self, dsn):
        self._dsn = dsn.replace("postgresql+psycopg://", "postgresql://", 1)

    @contextmanager
    def connection(self, *, autocommit=False):
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError:
            raise KnowledgeError("Install the knowledge postgres extra") from None
        try:
            with psycopg.connect(
                self._dsn, row_factory=dict_row, connect_timeout=5, autocommit=autocommit
            ) as conn:
                yield conn
        except psycopg.Error:
            raise KnowledgeError(
                "Knowledge database unavailable; check connection and run init-db"
            ) from None

    def initialize(self):
        with self.connection() as conn:
            conn.execute(files("soundsplit_knowledge").joinpath("schema.sql").read_text())

    @contextmanager
    def sync_lock(self, root_id):
        # Serialize the complete crawl/publish cycle to prevent an older snapshot winning a race.
        with self.connection(autocommit=True) as conn:
            row = conn.execute("SELECT pg_try_advisory_lock(hashtextextended(%s, 0)) AS locked",
                               ("soundsplit-knowledge:" + root_id,)).fetchone()
            if not row["locked"]:
                raise KnowledgeError("Another synchronization is already running for this root")
            try:
                yield
            finally:
                conn.execute("SELECT pg_advisory_unlock(hashtextextended(%s, 0))",
                             ("soundsplit-knowledge:" + root_id,))

    def fingerprints(self, root_id):
        with self.connection() as conn:
            rows = conn.execute(
                """SELECT page_id, content_hash FROM knowledge.documents
                   WHERE root_id=%s AND profile=%s""",
                (root_id, PROFILE),
            ).fetchall()
        return {str(r["page_id"]): r["content_hash"] for r in rows}

    def publish(self, root_id, indexed, synced_at):
        with self.connection() as conn:
            from psycopg.types.json import Jsonb

            # Only a complete crawl may deactivate pages no longer in the authorized tree.
            conn.execute("UPDATE knowledge.documents SET active=false WHERE root_id=%s", (root_id,))
            for item in indexed:
                doc = item.document
                conn.execute("""
                    INSERT INTO knowledge.documents
                        (root_id,page_id,title,page_url,edited_at,last_synced_at,
                         document_type,status,confidence,ids,tags,metadata,warnings,
                         content_hash,profile,active)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true)
                    ON CONFLICT (root_id,page_id) DO UPDATE SET
                        title=excluded.title,page_url=excluded.page_url,
                        edited_at=excluded.edited_at,
                        last_synced_at=excluded.last_synced_at,document_type=excluded.document_type,
                        status=excluded.status,confidence=excluded.confidence,ids=excluded.ids,
                        tags=excluded.tags,metadata=excluded.metadata,warnings=excluded.warnings,
                        content_hash=excluded.content_hash,profile=excluded.profile,active=true
                    """, (
                        root_id, doc.page_id, doc.title, doc.url, doc.edited_at, synced_at,
                        doc.document_type, doc.status, doc.confidence, doc.ids, doc.tags,
                        Jsonb(doc.metadata), Jsonb(doc.warnings), item.content_hash, PROFILE,
                    ))
                if item.chunks is None:
                    continue
                validate_vectors(item.vectors, len(item.chunks))
                conn.execute("DELETE FROM knowledge.chunks WHERE root_id=%s AND page_id=%s",
                             (root_id, doc.page_id))
                for chunk, vector in zip(item.chunks, item.vectors, strict=True):
                    conn.execute("""
                        INSERT INTO knowledge.chunks
                            (root_id,page_id,chunk_id,content,block_id,headings,knowledge_type,
                             embedding,search_text)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s::vector,to_tsvector('simple', %s))
                        """, (
                            root_id, doc.page_id, chunk.id, chunk.text, chunk.block_id,
                            list(chunk.headings), chunk.knowledge_type, json.dumps(vector),
                            embedding_text(doc, chunk),
                        ))
            count = conn.execute("""
                SELECT count(*) AS n FROM knowledge.chunks c JOIN knowledge.documents d
                USING(root_id,page_id) WHERE d.root_id=%s AND d.active
                """, (root_id,)).fetchone()["n"]
            conn.execute("""
                INSERT INTO knowledge.sync_state VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT(root_id) DO UPDATE SET profile=excluded.profile,
                    last_synced_at=excluded.last_synced_at,document_count=excluded.document_count,
                    chunk_count=excluded.chunk_count
                """, (root_id, PROFILE, synced_at, len(indexed), count))
        return count

    def search(self, root_id, query, vector, filters: SearchFilters, *, limit=8,
               max_age_hours=24, min_similarity=0.45):
        root_id = page_id(root_id)
        validate_vectors([vector], 1)
        if not query.strip() or not 1 <= limit <= 20 or not 1 <= max_age_hours <= 168:
            raise ValueError("Invalid query, result limit, or index freshness limit")
        clauses = ["d.root_id=%(root)s", "d.active", "d.profile=%(profile)s"]
        params = {"root": root_id, "profile": PROFILE, "query": query, "vector": json.dumps(vector),
                  "limit": limit, "candidates": max(50, limit * 10), "similarity": min_similarity,
                  "query_ids": sorted(set(i.upper() for i in IDS.findall(query)))}
        for key, column, values in [
            ("ids", "d.ids", filters.ids), ("tags", "d.tags", filters.tags),
        ]:
            if values:
                clauses.append(f"{column} {'@>' if key == 'tags' else '&&'} %({key})s::text[]")
                params[key] = [v.upper() for v in values] if key == "ids" else values
        for key, column, values in [
            ("types", "d.document_type", filters.document_types),
            ("knowledge_types", "c.knowledge_type", filters.knowledge_types),
            ("statuses", "d.status", filters.statuses),
            ("confidence", "d.confidence", filters.confidence),
        ]:
            if values:
                clauses.append(f"lower({column}) = ANY(%({key})s::text[])")
                params[key] = [v.casefold() for v in values]
        if filters.edited_after:
            clauses.append("d.edited_at >= %(edited_after)s")
            params["edited_after"] = filters.edited_after
        if filters.accepted_decisions_only:
            clauses += ["d.document_type='decision'", "lower(d.status)='accepted'",
                        "c.knowledge_type='decision'"]
        where = " AND ".join(clauses)
        with self.connection() as conn:
            # Read state and results from the same committed snapshot during concurrent publication.
            conn.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
            state = conn.execute(
                "SELECT * FROM knowledge.sync_state WHERE root_id=%s", (root_id,)
            ).fetchone()
            if not state:
                raise KnowledgeError("Knowledge index is empty; run sync first")
            if state["profile"] != PROFILE:
                raise KnowledgeError("Knowledge index profile is outdated; run sync first")
            expiry = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
            if state["last_synced_at"] < expiry:
                raise KnowledgeError("Knowledge index is stale; synchronize Notion before querying")
            rows = conn.execute(f"""
                WITH eligible AS MATERIALIZED (
                    SELECT c.*,d.title,d.page_url,d.edited_at,d.last_synced_at,d.document_type,
                           d.status,d.confidence,d.ids,d.tags,d.metadata,d.warnings,
                           1 - (c.embedding <=> %(vector)s::vector) AS cosine_similarity,
                           ts_rank_cd(
                               c.search_text,websearch_to_tsquery('simple',%(query)s)
                           ) AS lexical,
                           (d.ids && %(query_ids)s::text[]) AS exact_id
                    FROM knowledge.chunks c JOIN knowledge.documents d USING(root_id,page_id)
                    WHERE {where}
                ), semantic AS (
                    SELECT chunk_id,
                           row_number() OVER(ORDER BY cosine_similarity DESC,chunk_id) AS rank
                    FROM eligible WHERE cosine_similarity >= %(similarity)s
                    ORDER BY cosine_similarity DESC,chunk_id LIMIT %(candidates)s
                ), lexical AS (
                    SELECT chunk_id,
                           row_number() OVER(ORDER BY exact_id DESC,lexical DESC,chunk_id) AS rank
                    FROM eligible WHERE lexical > 0 OR exact_id
                    ORDER BY exact_id DESC,lexical DESC,chunk_id LIMIT %(candidates)s
                ), scores AS (
                    SELECT coalesce(s.chunk_id,l.chunk_id) AS chunk_id,
                           coalesce(1.0/(60+s.rank),0)+coalesce(1.0/(60+l.rank),0) AS score
                    FROM semantic s FULL OUTER JOIN lexical l USING(chunk_id)
                )
                SELECT e.page_id,e.chunk_id,e.content,e.block_id,e.headings,e.knowledge_type,
                       e.title,e.page_url,e.edited_at,e.last_synced_at,e.document_type,e.status,
                       e.confidence,e.ids,e.tags,e.metadata,e.warnings,e.cosine_similarity,s.score
                FROM scores s JOIN eligible e USING(chunk_id)
                ORDER BY e.exact_id DESC,s.score DESC,e.edited_at DESC,e.chunk_id LIMIT %(limit)s
                """, params).fetchall()
        results = []
        for row in rows:
            row["page_id"] = str(row["page_id"])
            row["score"] = float(row["score"])
            row["citation_url"] = (
                row["page_url"].split("#")[0] + "#" + row["block_id"].replace("-", "")
                if row["block_id"]
                else row["page_url"]
            )
            row["normative"] = (row["document_type"] == "decision"
                                and (row["status"] or "").casefold() == "accepted"
                                and row["knowledge_type"] == "decision")
            results.append(row)
        return {"query": query, "results": results, "profile": PROFILE,
                "last_synced_at": state["last_synced_at"],
                "document_count": state["document_count"],
                "empty_reason": "no_matching_evidence" if not results else None}
