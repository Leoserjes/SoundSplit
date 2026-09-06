from datetime import datetime, timezone

from .chunking import chunk_document, embedding_text, fingerprint
from .embeddings import validate_vectors
from .models import PROFILE, IndexedDocument, KnowledgeError
from .notion import page_id


def synchronize(reader, store, embedder, root_id: str, *, force=False):
    root_id = page_id(root_id)
    if embedder.profile != PROFILE:
        raise KnowledgeError("Synchronization embedder must match the index profile")
    with store.sync_lock(root_id):
        # Timestamp the start, not the end: a slow crawl does not make old source reads look fresh.
        synced_at = datetime.now(timezone.utc)
        documents = reader.crawl(root_id)
        if not documents or not any(d.page_id == root_id for d in documents):
            raise KnowledgeError("Notion root missing from crawl; index was not published")
        known = {} if force else store.fingerprints(root_id)
        indexed = []
        updated = 0
        warnings = []
        for doc in documents:
            if doc.root_id != root_id:
                raise KnowledgeError("Document outside requested root; index was not published")
            digest = fingerprint(doc)
            warnings.extend({"page_id": doc.page_id, "warning": w} for w in doc.warnings)
            if known.get(doc.page_id) == digest:
                indexed.append(IndexedDocument(doc, digest, None, None))
                continue
            chunks = chunk_document(doc)
            texts = [embedding_text(doc, chunk) for chunk in chunks]
            vectors = []
            for start in range(0, len(texts), 16):
                batch = texts[start:start + 16]
                vectors.extend(validate_vectors(embedder.encode(batch), len(batch)))
            indexed.append(IndexedDocument(doc, digest, chunks, vectors))
            updated += 1
        chunk_count = store.publish(root_id, indexed, synced_at)
    return {"documents": len(documents), "updated": updated, "unchanged": len(documents) - updated,
            "chunks": chunk_count, "last_synced_at": synced_at.isoformat(), "warnings": warnings,
            "profile": PROFILE}
