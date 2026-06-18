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
