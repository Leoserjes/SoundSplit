from functools import lru_cache

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.knowledge import KnowledgeSearchRequest, KnowledgeSearchResponse
from soundsplit_knowledge.embeddings import HttpEmbedder
from soundsplit_knowledge.models import KnowledgeError, SearchFilters
from soundsplit_knowledge.store import PostgresStore

router = APIRouter()


@lru_cache
def store():
    return PostgresStore(settings.knowledge_database_url)


@lru_cache
def embedder():
    return HttpEmbedder(settings.knowledge_embedding_url)


@router.post("/search", response_model=KnowledgeSearchResponse)
def search(request: KnowledgeSearchRequest) -> dict:
    try:
        query = request.query.strip()
        filters = SearchFilters(**request.filters.model_dump())
        vector = embedder().encode([query])[0]
        return store().search(settings.notion_knowledge_root_id, query, vector, filters,
                              limit=request.limit,
                              max_age_hours=settings.knowledge_max_age_hours,
                              min_similarity=settings.knowledge_min_similarity)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    except KnowledgeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
