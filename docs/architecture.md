# SoundSplit Architecture

This document describes the checked-in implementation. Priorities, sprint mapping, and proposed work belong in GitHub Projects and Issues.

## Current Components and Flow

```text
Tauri / React desktop -> FastAPI -> SQLite job repository
                                -> local upload and artifact storage
                                -> knowledge search -> PostgreSQL / pgvector + embedding service
```

The desktop submits local audio and displays the returned job and artifact metadata. Automatic status polling and artifact download controls are not implemented in the current UI. The API exposes artifact downloads independently.

### Jobs and Uploads

`POST /v1/jobs` creates a job from metadata. `POST /v1/jobs/upload` accepts a multipart `file` with a WAV, MP3, or FLAC filename, rejects empty content, and enforces a 100 MiB limit. Validation checks the extension and size; it does not decode or verify audio content.

`JobService` uses `SQLiteJobRepository` by default and `InMemoryJobRepository` in the test environment or an explicitly injected repository. The repository operates on `JobResponse` through `create_job(job)`, `get_job(job_id)`, `update_job(job)`, and `list_jobs(limit=50)`. See the [interface](../apps/api/app/repositories/base.py) for exact signatures. There is no public list-jobs endpoint yet.

Jobs are created with status `queued`. During creation, the service writes placeholder stem, MIDI, and MusicXML files and marks their metadata `ready`. These bytes are test placeholders, not usable musical output. There is no connected worker advancing jobs to completion. The separate `AudioPipeline` stub returns artifact names only.

Uploads are saved after job creation. Job persistence and file writes are not transactional; a storage failure can leave a job without its upload. This limitation is tracked in [Issue #37](https://github.com/Leoserjes/SoundSplit/issues/37).

### Local Storage

- `SQLITE_DB_PATH` defaults to `data/soundsplit.db`.
- `STORAGE_ROOT` defaults to `data`.
- Uploads live under `uploads/{job_id}/`; artifacts under `artifacts/{job_id}/`.
- Relative paths and `.env` resolution depend on the working directory. Start commands from the repository root for consistent local state.
- `LocalStorageService` implements the storage boundary; runtime data is ignored by Git.
- Artifact download resolves metadata and files by artifact ID. Prefer the returned `uri`; name fallback has a known limitation tracked in [Issue #32](https://github.com/Leoserjes/SoundSplit/issues/32).

### API Surface

```text
GET  /health
POST /v1/jobs
POST /v1/jobs/upload
GET  /v1/jobs/{job_id}
GET  /v1/jobs/{job_id}/artifacts
GET  /v1/jobs/{job_id}/artifacts/{artifact_id}/download
POST /v1/knowledge/search
```

Running API documentation is available at `/docs` and `/openapi.json`. Shared schemas live in [packages/contracts](../packages/contracts); implementation changes must be reviewed against those schemas.

### Knowledge Retrieval

The Notion Knowledge Base is the human-owned source for curated knowledge. A read-only synchronizer creates a rebuildable PostgreSQL/pgvector index with citations and source metadata. Search uses an embedding service and rejects stale indexes. This PostgreSQL database serves knowledge retrieval; job persistence currently uses SQLite.

The API imports `soundsplit_knowledge`, so the local package and its PostgreSQL driver are part of the standard installation. Embedding model dependencies and running the retrieval services are needed only for retrieval operations. See [setup and trust rules](knowledge-retrieval.md).

## Future Architecture

Remote audio workers, Redis queueing, PostgreSQL job persistence, S3-compatible audio storage, real separation/transcription, and PDF scores are intended evolution points. Infrastructure configuration or environment variables alone do not mean these integrations are active. Implementation scope and sequencing belong in GitHub Projects.
