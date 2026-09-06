import hashlib
import json
import re
from dataclasses import asdict

from .models import PROFILE, Chunk, Document

MARKERS = {
    "FACT": "evidence", "EVIDENCE": "evidence", "DECISION": "decision",
    "HYPOTHESIS": "hypothesis", "ASSUMPTION": "hypothesis",
    "OPEN QUESTION": "question", "QUESTION": "question", "UNKNOWN": "unspecified",
}


def explicit_type(text: str) -> str | None:
    match = re.match(r"^\s*(?:\*\*)?\[([A-Z ]+)\]", text)
    return MARKERS.get(match[1]) if match else None


def fingerprint(document: Document) -> str:
    payload = {"profile": PROFILE, "document": asdict(document)}
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(serialized).hexdigest()


def split_text(text: str, limit: int):
    """Bound long paragraphs without silently truncating the source."""
    while len(text) > limit:
        boundary = text.rfind(" ", 0, limit + 1)
        if boundary < limit // 2:
            boundary = limit
        yield text[:boundary].strip()
        text = text[boundary:].lstrip()
    if text.strip():
        yield text.strip()


def chunk_document(document: Document, limit: int = 1800) -> list[Chunk]:
    if limit < 100:
        raise ValueError("Chunk limit must be at least 100 characters")
    chunks = []
    # Keep Notion blocks as citation boundaries. Never merge different epistemic labels.
    for section in document.sections:
        active_type = section.knowledge_type
        # SSOT markers may occur on separate lines within the same Notion block.
        for segment in re.split(r"\n(?=\s*(?:\*\*)?\[[A-Z ]+\])", section.text):
            active_type = explicit_type(segment) or active_type
            for text in split_text(segment, limit):
                identity = f"{document.page_id}:{len(chunks)}:{text}:{active_type}"
                chunks.append(Chunk(
                    hashlib.sha256(identity.encode()).hexdigest(), text,
                    section.block_id, section.headings, active_type,
                ))
    return chunks


def embedding_text(document: Document, chunk: Chunk) -> str:
    context = " > ".join((document.title, *chunk.headings))
    identifiers = " ".join(document.ids)
    # Evidence labels travel into retrieval, but do not turn similarity into confidence.
    return f"{context}\n{identifiers}\n[{chunk.knowledge_type}]\n{chunk.text}"
