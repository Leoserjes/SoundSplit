from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.api.routes import knowledge as knowledge_routes
from app.main import app
from soundsplit_knowledge.models import DIMENSIONS, PROFILE, KnowledgeError

client = TestClient(app)


class Embedder:
    def encode(self, texts):
        return [[1.0] + [0.0] * (DIMENSIONS - 1) for _ in texts]


class Store:
    def search(self, root, query, vector, filters, **options):
        now = datetime.now(timezone.utc)
        return {"query": query, "profile": PROFILE, "last_synced_at": now,
                "document_count": 1, "empty_reason": None, "results": [{
                    "page_id": root, "chunk_id": "chunk", "title": "ADR-001",
                    "page_url": "https://notion.so/page",
                    "citation_url": "https://notion.so/page#block",
                    "content": "Use cited retrieval", "headings": ["Decision"],
                    "knowledge_type": "decision", "document_type": "decision",
                    "status": "Accepted", "confidence": None, "ids": ["ADR-001"],
                    "tags": ["audio-ai"], "edited_at": now, "last_synced_at": now,
                    "score": 0.03, "cosine_similarity": 0.8, "normative": True, "warnings": [],
                }]}


def test_knowledge_search_returns_citations(monkeypatch):
    monkeypatch.setattr(knowledge_routes, "embedder", lambda: Embedder())
    monkeypatch.setattr(knowledge_routes, "store", lambda: Store())

    response = client.post("/v1/knowledge/search", json={
        "query": "Qual decisão rege o retrieval?",
        "filters": {"accepted_decisions_only": True},
    })

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["citation_url"].endswith("#block")
    assert result["normative"] is True


def test_openapi_includes_knowledge_search():
    assert "/v1/knowledge/search" in client.get("/openapi.json").json()["paths"]


class UnavailableEmbedder:
    def encode(self, texts):
        raise KnowledgeError("Knowledge dependency is unreachable or returned invalid JSON")


def test_knowledge_dependency_failure_is_safe(monkeypatch):
    monkeypatch.setattr(knowledge_routes, "embedder", lambda: UnavailableEmbedder())

    response = client.post("/v1/knowledge/search", json={"query": "instrumentos"})

    assert response.status_code == 503
    assert "token" not in response.text.casefold()
    assert "postgresql" not in response.text.casefold()
