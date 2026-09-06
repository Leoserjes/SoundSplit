from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

MODEL = "BAAI/bge-m3"
MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
DIMENSIONS = 1024
# Changing normalization, chunking, pooling, or model requires a complete reindex.
PROFILE = f"notion-blocks-v1:chars-1800:{MODEL}@{MODEL_REVISION}:dense-normalized"


class KnowledgeError(RuntimeError):
    """An operational error with a message safe to display (no tokens or DSNs)."""


@dataclass(frozen=True)
class Section:
    text: str
    block_id: str | None = None
    headings: tuple[str, ...] = ()
    knowledge_type: str = "unspecified"


@dataclass
class Document:
    page_id: str
    root_id: str
    title: str
    url: str
    edited_at: str
    document_type: str = "page"
    status: str | None = None
    confidence: str | None = None
    ids: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    sections: list[Section] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    block_id: str | None
    headings: tuple[str, ...]
    knowledge_type: str


@dataclass
class IndexedDocument:
    document: Document
    content_hash: str
    # None means reuse the existing chunks for the unchanged fingerprint.
    chunks: list[Chunk] | None
    vectors: list[list[float]] | None


@dataclass
class SearchFilters:
    ids: list[str] = field(default_factory=list)
    document_types: list[str] = field(default_factory=list)
    knowledge_types: list[str] = field(default_factory=list)
    statuses: list[str] = field(default_factory=list)
    confidence: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    edited_after: datetime | None = None
    accepted_decisions_only: bool = False


class Embedder(Protocol):
    profile: str

    def encode(self, texts: list[str]) -> list[list[float]]: ...
