# SoundSplit Knowledge Retrieval

## Purpose

The Notion page `SoundSplit — Knowledge Base` remains the human-owned source of truth. This
component creates a read-only, rebuildable retrieval index for SoundSplit agents and products.
It does not write to Notion and it does not answer questions by itself. Consumers receive cited
passages and decide how to generate an answer.

```text
Notion page tree
  -> complete read-only crawl
  -> block-aware chunks + source metadata
  -> pinned multilingual BGE-M3 embeddings
  -> PostgreSQL lexical + pgvector index
  -> POST /v1/knowledge/search
  -> cited passages for an agent or UI
```

## Trust and retrieval rules

- The crawler starts at one configured root page and follows only child pages and rows from child
  databases. Relations and ordinary links do not expand the authorization boundary.
- Every result includes the Notion page URL, a block-level citation when possible, source edit and
  sync times, document IDs, status, confidence, tags, and epistemic type.
- `[EVIDENCE]`, `[HYPOTHESIS]`, and `[DECISION]` markers become separate chunks even when they are
  stored in one Notion block.
- `normative=true` requires all three conditions: a decision record, status `Accepted`, and a
  decision-labeled chunk.
- Similarity is a retrieval signal. It never changes source confidence or decision status.
- The API rejects stale indexes. The default maximum age is 24 hours.
- Attachments and externally sourced synced blocks are reported as warnings instead of being
  silently treated as indexed text.

## Components

| Component | Responsibility |
| --- | --- |
| `packages/knowledge` | Notion reader, chunking, embeddings, PostgreSQL store, and CLI |
| `workers/ai` knowledge extra | Local BGE-M3 inference process bound to loopback |
| `apps/api` | Validated search contract and cited retrieval endpoint |
| PostgreSQL `knowledge` schema | Derived documents, chunks, vectors, and sync state |

The model is pinned to `BAAI/bge-m3` revision
`5617a9f61b028005a4858fdac845db406aefb181`. The index profile includes the model revision and
chunking version. Any profile change requires reindexing.

## Local setup

Install all Python workspace packages into the repository virtual environment:

```powershell
.venv\Scripts\python.exe -m pip install -e packages\knowledge[postgres,embeddings,test] -e apps\api[test] -e workers\ai[test]
```

Start PostgreSQL with pgvector. New volumes initialize the knowledge schema automatically:

```powershell
docker compose up -d postgres
```

For an existing PostgreSQL volume, apply the idempotent schema once:

```powershell
.venv\Scripts\python.exe -m soundsplit_knowledge init-db
```

Start the local embedding process in one terminal. The first run downloads the pinned model:

```powershell
.venv\Scripts\python.exe -m soundsplit_knowledge serve-embeddings
```

Synchronize the Knowledge Base in another terminal. Prefer the environment variable in deployed
environments. The explicit MCP fallback is convenient for local development and the ignored config
must contain `mcpServers.notion.env.NOTION_TOKEN`:

```powershell
.venv\Scripts\python.exe -m soundsplit_knowledge sync --mcp-config .agents\mcp_config.json
```

The sync publishes all changes in one database transaction. A failed or incomplete crawl leaves the
previous index active. Unchanged pages reuse their existing chunks and vectors.

Start the API and query cited passages:

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir apps\api
```

```http
POST /v1/knowledge/search
Content-Type: application/json

{
  "query": "Qual decisão aceita define a arquitetura de transcrição?",
  "limit": 8,
  "filters": {
    "accepted_decisions_only": true,
    "tags": ["sheet-music"]
  }
}
```

An empty result returns `empty_reason: "no_matching_evidence"`. Consumers should state that the
indexed source has insufficient evidence rather than filling the gap from model memory.

## Operations

Run synchronization after reviewed Notion changes and at least once within the configured freshness
window. Only one sync per root runs at a time. Use `--force` after an embedding or chunking migration.

Useful configuration:

| Variable | Default | Meaning |
| --- | --- | --- |
| `NOTION_TOKEN` | none | Integration token with read access to the Knowledge Base |
| `NOTION_KNOWLEDGE_ROOT_ID` | SoundSplit root UUID | Allowed Notion subtree |
| `KNOWLEDGE_DATABASE_URL` | local SoundSplit PostgreSQL | Derived index database |
| `KNOWLEDGE_EMBEDDING_URL` | `http://127.0.0.1:8091` | Loopback embedding process |
| `KNOWLEDGE_MAX_AGE_HOURS` | `24` | Maximum accepted index age |
| `KNOWLEDGE_MIN_SIMILARITY` | `0.45` | Dense candidate threshold |

The embedding endpoint accepts local process traffic only and does not log source text or queries.
For cloud deployment, replace this process boundary with authenticated private networking before
allowing a non-loopback URL.
