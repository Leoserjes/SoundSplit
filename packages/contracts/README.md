# Contracts

Shared schemas for API payloads and job states.

The contracts here should stay small and stable. Frontend, backend, and workers can mirror these shapes in their own native types.

## Current Contracts

- `job.schema.json`: canonical analysis job response, including job status, source metadata, and artifact metadata.
- `upload.schema.json`: multipart upload request boundary for `POST /v1/jobs/upload`.

## Sprint 02 Upload Contract

`POST /v1/jobs/upload` accepts `multipart/form-data` with a single binary file part named `file`.

Rules:

- Supported filename extensions: `.wav`, `.mp3`, `.flac`.
- Maximum file size: 100 MB, represented as `104857600` bytes.
- Empty files are rejected.
- Uploaded bytes are validated and discarded after request handling during Sprint 02.
- The response is the existing `AnalysisJob` shape from `job.schema.json`.
- The returned job uses `source_type: "upload"`, `source_name` set to the uploaded filename, and `status: "queued"`.
