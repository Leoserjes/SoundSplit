from soundsplit_knowledge.chunking import chunk_document, fingerprint
from soundsplit_knowledge.models import Document, Section


def document(sections):
    return Document(
        page_id="11111111-1111-1111-1111-111111111111",
        root_id="22222222-2222-2222-2222-222222222222",
        title="ADR-001 Retrieval",
        url="https://www.notion.so/example",
        edited_at="2026-09-06T00:00:00Z",
        document_type="decision",
        status="Accepted",
        ids=["ADR-001"],
        sections=sections,
    )


def test_markers_are_kept_as_separate_epistemic_chunks():
    chunks = chunk_document(document([
        Section("[EVIDENCE] A benchmark result.\n[HYPOTHESIS] It may generalize.", block_id="b1")
    ]))

    assert [chunk.knowledge_type for chunk in chunks] == ["evidence", "hypothesis"]
    assert all(chunk.block_id == "b1" for chunk in chunks)


def test_long_sections_are_bounded_without_losing_text():
    source = " ".join(["music"] * 80)
    chunks = chunk_document(document([Section(source)]), limit=100)

    assert len(chunks) > 1
    assert " ".join(chunk.text for chunk in chunks) == source
    assert all(len(chunk.text) <= 100 for chunk in chunks)


def test_fingerprint_changes_with_source_or_index_profile():
    first = document([Section("one")])
    second = document([Section("two")])

    assert fingerprint(first) == fingerprint(first)
    assert fingerprint(first) != fingerprint(second)
