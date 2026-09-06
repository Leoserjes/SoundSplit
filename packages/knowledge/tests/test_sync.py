from contextlib import contextmanager

from soundsplit_knowledge.chunking import fingerprint
from soundsplit_knowledge.models import DIMENSIONS, PROFILE, Document, Section
from soundsplit_knowledge.sync import synchronize

ROOT = "11111111-1111-1111-1111-111111111111"


class Reader:
    def crawl(self, root_id):
        return [Document(ROOT, ROOT, "Root", "https://notion.so/root", "2026-09-06T00:00:00Z",
                         sections=[Section("[EVIDENCE] Source text")])]


class Store:
    def __init__(self, known=None):
        self.known = known or {}
        self.published = None

    @contextmanager
    def sync_lock(self, _):
        yield

    def fingerprints(self, _):
        return self.known

    def publish(self, root, indexed, synced_at):
        self.published = indexed
        return sum(len(i.chunks or []) for i in indexed)


class Embedder:
    profile = PROFILE

    def __init__(self):
        self.calls = 0

    def encode(self, texts):
        self.calls += 1
        return [[1.0] + [0.0] * (DIMENSIONS - 1) for _ in texts]


def test_sync_embeds_changed_documents():
    store, embedder = Store(), Embedder()
    result = synchronize(Reader(), store, embedder, ROOT)

    assert result["documents"] == 1
    assert result["updated"] == 1
    assert result["chunks"] == 1
    assert embedder.calls == 1
    assert store.published[0].vectors[0][0] == 1.0


def test_sync_reuses_unchanged_document_chunks():
    source = Reader().crawl(ROOT)[0]
    store, embedder = Store({ROOT: fingerprint(source)}), Embedder()
    result = synchronize(Reader(), store, embedder, ROOT)

    assert result["unchanged"] == 1
    assert embedder.calls == 0
    assert store.published[0].chunks is None
