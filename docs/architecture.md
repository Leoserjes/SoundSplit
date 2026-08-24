# SoundSplit Architecture

## Overview

harmonIA is designed as a desktop-first music engineering workflow. The desktop app is the user's workspace, while the backend and AI workers handle heavy processing.

```text
Tauri Desktop App
  -> FastAPI API
  -> Job Queue
  -> AI Worker
  -> Object Storage
  -> API Result Metadata
  -> Desktop Downloads / Preview
```

## Components

### Desktop App

The desktop app owns the professional user experience:

- Project creation and local workspace organization
- Drag-and-drop audio import
- Job submission and progress display
- Playback previews for stems
- Download/export of stems, MIDI, MusicXML, and PDF scores

### API

The FastAPI service owns product orchestration:

- Authentication and licensing later
- Project and job metadata
- Upload endpoints
- Job creation and status
- Result listing
- Signed URLs or direct downloads

### AI Worker

The worker owns the long-running music pipeline:

- Audio normalization
- Stem separation
- Instrument detection
- Pitch/onset transcription
- MIDI generation
- MusicXML/PDF score generation

The first MVP should use proven models and libraries before training SoundSplit-specific models.

### Storage

PostgreSQL stores metadata. Object storage stores large artifacts:

- Original audio
- Normalized audio
- Stems
- MIDI
- MusicXML
- PDF scores
- Worker logs/artifacts

Redis is used for queueing and short-lived job state.

## MVP Job Lifecycle

```text
created
  -> uploading
  -> queued
  -> processing
  -> completed
```

Failure path:

```text
created
  -> queued
  -> processing
  -> failed
```

## Initial API Surface

```text
GET  /health
POST /v1/jobs
POST /v1/jobs/upload
GET  /v1/jobs/{job_id}
GET  /v1/jobs/{job_id}/artifacts
```

The first version can use local files and mocked worker output, then move to real object storage and model inference.

## Sprint 02 Upload Contract

Sprint 02 adds the first real local ingestion boundary without introducing persistence, queueing, or real AI processing.

Endpoint:

```text
POST /v1/jobs/upload
Content-Type: multipart/form-data
Form field: file
Response: AnalysisJob
```

Behavior:

- Accept one local audio file through the multipart `file` part.
- Accept `.wav`, `.mp3`, and `.flac` filenames up to 100 MB.
- Reject unsupported extensions, empty files, and oversized files with clear client-facing errors.
- Create an in-memory job with `source_type: "upload"`, `source_name` set to the uploaded filename, and `status: "queued"`.
- Return the same `AnalysisJob` response shape used by `POST /v1/jobs`.
- Discard uploaded bytes after validation and job creation for this sprint.

Boundary decisions:

- Storage, Redis queueing, audio decoding, normalization, and real AI processing remain deferred.
- The desktop client submits the file only when the user starts analysis.
- The shared upload request boundary is documented in `packages/contracts/upload.schema.json`.

## Sprint 04 Durable Architecture & Storage Boundaries

Sprint 04 establishes durable job persistence and local storage boundaries so jobs and uploaded files survive API process restarts without requiring cloud infrastructure yet.

### 1. Job Repository Boundary (`JobRepository`)

All job state transitions and metadata access are encapsulated behind an abstract repository interface:

```python
class JobRepository(ABC):
    @abstractmethod
    def create_job(self, job: AnalysisJob) -> AnalysisJob: ...
    @abstractmethod
    def get_job(self, job_id: str) -> Optional[AnalysisJob]: ...
    @abstractmethod
    def update_job(self, job_id: str, updates: dict) -> Optional[AnalysisJob]: ...
    @abstractmethod
    def list_jobs(self, limit: int = 50) -> list[AnalysisJob]: ...
    @abstractmethod
    def get_artifacts(self, job_id: str) -> list[ArtifactMetadata]: ...
```

- **Development Default:** `SQLiteJobRepository` persists to a local SQLite database at `data/soundsplit.db`.
- **Testing Seam:** `InMemoryJobRepository` is injected in test fixtures to guarantee deterministic, isolated, fast unit tests.
- **Production Path:** `PostgreSQLJobRepository` (via `DATABASE_URL` with SQLAlchemy/asyncpg).

### 2. Storage Service Boundary (`StorageService`)

All audio uploads and generated artifacts are stored via an abstract storage interface:

```python
class StorageService(ABC):
    @abstractmethod
    def save_upload(self, job_id: str, filename: str, content: bytes) -> str: ...
    @abstractmethod
    def get_upload_path(self, job_id: str) -> Optional[Path]: ...
    @abstractmethod
    def save_artifact(self, job_id: str, artifact_name: str, content: bytes) -> str: ...
    @abstractmethod
    def get_artifact_path(self, job_id: str, artifact_name: str) -> Optional[Path]: ...
    @abstractmethod
    def delete_job_files(self, job_id: str) -> bool: ...
```

- **Local Storage Root:** `data/` (configured via `STORAGE_ROOT` in `.env`, defaults to `./data`).
  - Uploads: `data/uploads/{job_id}/{filename}`
  - Artifacts: `data/artifacts/{job_id}/{artifact_name}`
- **Security & Safety:**
  - `data/` is strictly ignored by `.gitignore`.
  - Raw uploads are rejected if they exceed 100 MB or have invalid extensions (`.wav`, `.mp3`, `.flac`).
  - Path traversal protections ensure filenames cannot escape the job storage directory.
- **Future Cloud Evolution:** `S3StorageService` will implement this exact interface with MinIO/AWS S3 without changing API route signatures.

### 3. Artifact Metadata & Lifecycle

Artifacts transition through explicit statuses:
`pending` ➔ `processing` ➔ `ready` (or `failed`)

- Artifact listing endpoint: `GET /v1/jobs/{job_id}/artifacts`
- Artifact download endpoint: `GET /v1/jobs/{job_id}/artifacts/{artifact_id}/download` (or by name `GET /v1/jobs/{job_id}/artifacts/{name}`)
- In Sprint 04, when an analysis job is marked complete, mocked/sample artifacts are materialized in storage to allow end-to-end testing of the download flow before the real PyTorch stem separation pipeline in Sprint 05/06.

### 4. Quality & Contract Verification
- All routes continue to strictly comply with `packages/contracts/job.schema.json` and `packages/contracts/upload.schema.json`.
- FastAPI Swagger UI at `/docs` and OpenAPI schema at `/openapi.json` serve as the living documentation for all route contracts.
