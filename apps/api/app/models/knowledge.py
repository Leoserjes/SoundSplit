from datetime import datetime

from pydantic import BaseModel, Field


class KnowledgeFilters(BaseModel):
    ids: list[str] = Field(default_factory=list, max_length=20)
    document_types: list[str] = Field(default_factory=list, max_length=10)
    knowledge_types: list[str] = Field(default_factory=list, max_length=10)
    statuses: list[str] = Field(default_factory=list, max_length=10)
    confidence: list[str] = Field(default_factory=list, max_length=10)
    tags: list[str] = Field(default_factory=list, max_length=20)
    edited_after: datetime | None = None
    accepted_decisions_only: bool = False


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    limit: int = Field(default=8, ge=1, le=20)
    filters: KnowledgeFilters = Field(default_factory=KnowledgeFilters)


class KnowledgeCitation(BaseModel):
    page_id: str
    chunk_id: str
    title: str
    page_url: str
    citation_url: str
    content: str
    headings: list[str]
    knowledge_type: str
    document_type: str
    status: str | None
    confidence: str | None
    ids: list[str]
    tags: list[str]
    edited_at: datetime
    last_synced_at: datetime
    score: float
    cosine_similarity: float
    normative: bool
    warnings: list[str]


class KnowledgeSearchResponse(BaseModel):
    query: str
    results: list[KnowledgeCitation]
    profile: str
    last_synced_at: datetime
    document_count: int
    empty_reason: str | None
