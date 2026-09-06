"""Read-only traversal of one explicitly authorized Notion page tree."""
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote, urlencode
from uuid import UUID

from .chunking import explicit_type
from .http import json_request
from .models import Document, KnowledgeError, Section

NOTION_VERSION = "2025-09-03"
IDS = re.compile(r"\b(?:PAPER|ADR|FIND|EXP|TASK|P|F|E|D)-\d+\b", re.I)


def page_id(value: str) -> str:
    try:
        return str(UUID(value))
    except (ValueError, TypeError, AttributeError):
        raise KnowledgeError("Notion root must be a page UUID") from None


def read_token(mcp_config: str | None = None) -> str:
    token = os.getenv("NOTION_TOKEN", "")
    if not token and mcp_config:
        try:
            config = json.loads(Path(mcp_config).read_text(encoding="utf-8-sig"))
            token = config["mcpServers"]["notion"]["env"]["NOTION_TOKEN"]
        except (OSError, ValueError, KeyError, TypeError):
            raise KnowledgeError("Cannot read NOTION_TOKEN from the specified MCP config") from None
    if not isinstance(token, str) or not token.strip():
        raise KnowledgeError("Set NOTION_TOKEN or explicitly supply --mcp-config")
    return token.strip()


def plain(items) -> str:
    return "".join(item.get("plain_text", item.get("text", {}).get("content", ""))
                   for item in items or [])


def property_value(prop):
    kind = prop.get("type")
    value = prop.get(kind)
    if kind in {"title", "rich_text"}:
        return plain(value)
    if kind in {"select", "status"}:
        return value.get("name") if value else None
    if kind == "multi_select":
        return [v["name"] for v in value or []]
    if kind == "relation":
        return [v["id"] for v in value or []]
    if kind == "unique_id" and value:
        if value.get("prefix"):
            return f"{value['prefix']}-{value['number']}"
        return str(value["number"])
    if kind in {"url", "number", "checkbox", "date", "created_time", "last_edited_time"}:
        return value
    if kind == "formula" and value:
        return value.get(value.get("type"))
    return None


def document_type(name: str) -> str:
    name = name.casefold()
    for keys, result in [(('paper',), 'paper'), (('finding',), 'finding'),
                         (('experiment',), 'experiment'), (('decision', 'adr'), 'decision'),
                         (('roadmap', 'task'), 'task')]:
        if any(key in name for key in keys):
            return result
    return "page"


class NotionReader:
    def __init__(self, token: str, *, max_pages=2000, request=json_request, interval=0.35):
        self._token = token
        self.max_pages = max_pages
        self.request = request
        self.interval = interval
        self._last_request = 0.0

    def get(self, path, body=None):
        time.sleep(max(0, self.interval - (time.monotonic() - self._last_request)))
        self._last_request = time.monotonic()
        return self.request("https://api.notion.com/v1/" + path,
                            headers={"Authorization": "Bearer " + self._token,
                                     "Notion-Version": NOTION_VERSION},
                            body=body, attempts=4)

    def paginate(self, path, *, query=False):
        cursor = None
        seen = set()
        while True:
            params = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            result = self.get(path, params) if query else self.get(path + "?" + urlencode(params))
            yield from result["results"]
            if not result.get("has_more"):
                return
            cursor = result.get("next_cursor")
            if not cursor or cursor in seen:
                raise KnowledgeError("Notion pagination was incomplete; index was not published")
            seen.add(cursor)

    def crawl(self, root_id: str) -> list[Document]:
        root_id = page_id(root_id)
        queue = [(root_id, "page")]
        visited = set()
        databases = set()
        documents = []
        while queue:
            current_id, kind = queue.pop(0)
            current_id = page_id(current_id)
            if current_id in visited:
                continue
            if len(visited) >= self.max_pages:
                raise KnowledgeError("Notion page limit reached; index was not published")
            visited.add(current_id)
            page = self.get(f"pages/{current_id}")
            if page.get("archived") or page.get("in_trash"):
                if current_id == root_id:
                    raise KnowledgeError("Notion root is archived; index was not published")
                continue
            props = page.get("properties", {})
            values = {}
            relations = {}
            for name, prop in props.items():
                # Page objects truncate some rich text and relations; retrieve full property lists.
                if prop.get("type") in {"rich_text", "title", "relation"} and (
                    prop.get("has_more") or len(prop.get(prop["type"], [])) >= 25
                ):
                    key = prop["type"]
                    path = f"pages/{current_id}/properties/{quote(prop['id'], safe='%')}"
                    items = list(self.paginate(path))
                    prop = {**prop, key: [item[key] for item in items]}
                value = property_value(prop)
                if value is not None:
                    values[name] = value
                if prop.get("type") == "relation":
                    relations[name] = value or []
            title = next((values.get(k, "") for k, v in props.items()
                          if v["type"] == "title"), "Untitled") or "Untitled"
            aliases = IDS.findall(title)
            for key, prop in props.items():
                if prop.get("type") == "unique_id" or key.casefold() == "id" or key.endswith(" ID"):
                    if values.get(key) is not None:
                        aliases.append(str(values[key]))
            lowered = {k.casefold(): v for k, v in values.items()}
            doc = Document(
                current_id, root_id, title,
                page.get("url") or f"https://www.notion.so/{current_id.replace('-', '')}",
                page["last_edited_time"], kind,
                status=lowered.get("status"),
                confidence=str(lowered["confidence"]) if "confidence" in lowered else None,
                ids=sorted(set(alias.upper() for alias in aliases)),
                tags=lowered.get("tags", []),
                metadata={"properties": values, "relations": relations,
                          "created_at": page.get("created_time")},
            )
            default_type = "evidence" if kind == "paper" else "unspecified"
            if kind == "finding":
                declared = next(
                    (
                        lowered.get(key)
                        for key in ("knowledge type", "finding type", "type")
                        if lowered.get(key)
                    ),
                    None,
                )
                if isinstance(declared, str):
                    default_type = {
                        "evidence": "evidence", "fact": "evidence", "hypothesis": "hypothesis",
                        "assumption": "hypothesis", "question": "question",
                    }.get(declared.casefold(), "unspecified")
            # Database records often keep their actual content in properties, not page blocks.
            for name, value in values.items():
                if props[name]["type"] in {"rich_text", "url"} and value:
                    field_type = default_type
                    lowered_name = name.casefold()
                    if "hypoth" in lowered_name or "assumption" in lowered_name:
                        field_type = "hypothesis"
                    elif kind == "decision" and lowered_name == "decision":
                        field_type = "decision"
                    elif kind == "experiment" and "result" in lowered_name:
                        field_type = "evidence"
                    doc.sections.append(Section(f"{name}: {value}", headings=("Properties",),
                                                knowledge_type=explicit_type(value) or field_type))
            self._blocks(current_id, doc, queue, databases, default_type=default_type)
            if not doc.sections:
                doc.sections.append(Section(title, knowledge_type=default_type))
            documents.append(doc)
        return documents

    def _blocks(self, block_id, doc, queue, databases, *, headings=(), default_type="unspecified",
                depth=0, ancestors=frozenset()):
        if depth > 64 or block_id in ancestors:
            raise KnowledgeError("Notion block recursion limit reached; index was not published")
        ancestors = ancestors | {block_id}
        active_headings = list(headings)
        active_type = default_type
        for block in self.paginate(f"blocks/{block_id}/children"):
            if block.get("archived") or block.get("in_trash"):
                continue
            kind = block["type"]
            body = block.get(kind, {})
            if kind == "child_page":
                queue.append((block["id"], "page"))
                continue
            if kind == "child_database":
                database_id = block["id"]
                if database_id in databases:
                    continue
                databases.add(database_id)
                database = self.get(f"databases/{database_id}")
                for source in database.get("data_sources", []):
                    source_type = document_type(source.get("name") or plain(database.get("title")))
                    for item in self.paginate(f"data_sources/{source['id']}/query", query=True):
                        queue.append((item["id"], source_type))
                if "data_sources" not in database:
                    raise KnowledgeError(
                        "Notion database returned no data sources; sync incomplete"
                    )
                continue
            # Links and relations do not extend the authorized tree.
            if kind == "synced_block" and body.get("synced_from"):
                doc.warnings.append(f"external_synced_block:{block['id']}")
                continue
            text = plain(body.get("rich_text"))
            if kind.startswith("heading_"):
                level = int(kind[-1])
                active_headings = active_headings[:level - 1] + [text]
                active_type = explicit_type(text) or default_type
            elif kind == "table_row":
                text = " | ".join(plain(cell) for cell in body.get("cells", []))
            elif kind == "equation":
                text = body.get("expression", "")
            elif kind in {"bookmark", "link_preview", "embed"}:
                text = " ".join(filter(None, [body.get("url"), plain(body.get("caption"))]))
            elif kind in {"image", "file", "pdf", "audio", "video"}:
                text = plain(body.get("caption"))
                doc.warnings.append(f"attachment_not_extracted:{block['id']}")
            elif kind == "unsupported":
                doc.warnings.append(f"unsupported_block:{block['id']}")
            if text:
                doc.sections.append(Section(text, block["id"], tuple(active_headings),
                                            explicit_type(text) or active_type))
            if block.get("has_children"):
                self._blocks(block["id"], doc, queue, databases, headings=tuple(active_headings),
                             default_type=active_type, depth=depth + 1, ancestors=ancestors)
