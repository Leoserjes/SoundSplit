from soundsplit_knowledge.notion import NotionReader, page_id

ROOT = "11111111-1111-1111-1111-111111111111"
CHILD = "22222222-2222-2222-2222-222222222222"
DATABASE = "33333333-3333-3333-3333-333333333333"
SOURCE = "44444444-4444-4444-4444-444444444444"
ROW = "55555555-5555-5555-5555-555555555555"


def rich(text):
    return [{"plain_text": text}]


class Reader(NotionReader):
    def __init__(self):
        super().__init__("not-a-real-token", interval=0)

    def get(self, path, body=None):
        if path == f"pages/{ROOT}":
            return page(ROOT, "SoundSplit Knowledge Base")
        if path == f"pages/{CHILD}":
            return page(CHILD, "Product & Vision")
        if path == f"pages/{ROW}":
            return page(ROW, "ADR-001 Decision", status="Accepted")
        if path == f"databases/{DATABASE}":
            return {"title": rich("Decisions / ADRs"),
                    "data_sources": [{"id": SOURCE, "name": "Decisions / ADRs"}]}
        raise AssertionError(path)

    def paginate(self, path, *, query=False):
        mapping = {
            f"blocks/{ROOT}/children": [
                {"id": CHILD, "type": "child_page", "child_page": {}, "has_children": True},
                {"id": DATABASE, "type": "child_database", "child_database": {},
                 "has_children": False},
            ],
            f"blocks/{CHILD}/children": [{
                "id": "c1", "type": "paragraph", "paragraph": {"rich_text": rich("Vision")},
                "has_children": False,
            }],
            f"blocks/{ROW}/children": [{
                "id": "r1", "type": "paragraph",
                "paragraph": {"rich_text": rich("[DECISION] Use citations")},
                "has_children": False,
            }],
            f"data_sources/{SOURCE}/query": [{"id": ROW}],
        }
        yield from mapping.get(path, [])


def page(identifier, title, status=None):
    properties = {"Title": {"id": "title", "type": "title", "title": rich(title)}}
    if status:
        properties["Status"] = {"id": "status", "type": "select",
                                "select": {"name": status}}
        properties["Context"] = {"id": "ctx", "type": "rich_text",
                                 "rich_text": rich("Problem context")}
        properties["Decision"] = {"id": "decision", "type": "rich_text",
                                  "rich_text": rich("Use citations")}
    return {"id": identifier, "url": "https://www.notion.so/" + identifier,
            "last_edited_time": "2026-09-06T00:00:00Z", "created_time": "2026-09-05T00:00:00Z",
            "archived": False, "in_trash": False, "properties": properties}


def test_crawl_stays_inside_explicit_tree_and_types_database_rows():
    documents = Reader().crawl(ROOT)

    assert {doc.page_id for doc in documents} == {ROOT, CHILD, ROW}
    decision = next(doc for doc in documents if doc.page_id == ROW)
    assert decision.document_type == "decision"
    assert decision.status == "Accepted"
    assert decision.ids == ["ADR-001"]
    property_types = {section.text.split(":", 1)[0]: section.knowledge_type
                      for section in decision.sections if section.headings == ("Properties",)}
    assert property_types == {"Context": "unspecified", "Decision": "decision"}
    assert decision.sections[-1].knowledge_type == "decision"
    assert all(doc.root_id == page_id(ROOT) for doc in documents)
