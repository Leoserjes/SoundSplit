# Sprint 02: v0.3.0 Local Audio Upload

## Sprint Summary

Duration: 14 calendar days
Planned start: 2026-06-13
Planned end: 2026-06-26
Release target: `v0.3.0`
Sprint owner: Maestro - Product Manager
Delivery coordinator: Atlas - Agent Manager

## Central Objective

Complete the first real desktop ingestion loop: the user selects or drops a local audio file in harmonIA, submits it to the FastAPI backend, and receives a visible mocked analysis job tied to the selected file.

This sprint validates local audio ingestion without introducing storage infrastructure or real AI processing. The backend validates the upload, creates in-memory job metadata, and discards file bytes after the request.

## Success Metrics

Product success:

- User can select a local audio file through the desktop UI.
- User can drag and drop a local audio file into the desktop UI.
- UI shows the selected filename before submission.
- UI shows clear validation, loading, success, and error states.
- Returned job summary uses the selected source filename.

Engineering success:

- Desktop submits audio through an isolated multipart API client.
- Backend accepts `.wav`, `.mp3`, and `.flac` files up to 100 MB.
- Backend rejects unsupported extensions, empty files, and oversized uploads.
- Existing job fetch and artifact routes remain stable.
- Uploaded file bytes are not persisted in this sprint.

Quality success:

- Backend upload validation paths have unit tests.
- Frontend file selection, drag-and-drop, submission, and error states have unit tests.
- QA reviews developer unit tests and adds regression coverage.
- Desktop build, frontend tests, backend/worker tests, and browser smoke pass.

Release success:

- All implementation cards are complete or explicitly deferred.
- Release Coordinator can recommend tagging `v0.3.0`.
- Existing Sprint 3 distribution backlog remains deferred.

## Scope

In:

- Local audio selection.
- Desktop drag-and-drop.
- Multipart upload to FastAPI.
- Filename, extension, and size validation.
- In-memory mocked job creation using the uploaded filename.
- Unit tests and QA review.
- Release notes for `v0.3.0`.

Out:

- File persistence or object storage.
- Audio decoding or normalization.
- Redis queue integration.
- PostgreSQL persistence.
- Real stem separation or transcription.
- YouTube or Spotify ingestion.
- Offline mode and distribution hardening.

## Product Rules

- Supported files: `.wav`, `.mp3`, and `.flac`.
- Maximum upload size: 100 MB.
- Empty files must be rejected.
- The selected file remains local until the user clicks the analysis action.
- Selecting a different file replaces the previous selection before submission.
- After a successful upload, the UI renders the job ID, queued status, source filename, and mocked artifacts.
- Validation errors must be short and actionable.

## Cards

### SS2-001: Define Local Audio Upload Requirements

Agent Owner: Maestro
Supporting: Atlas, Ada
Status: Ready

Value:

The team needs precise ingestion behavior before implementation starts.

Acceptance Criteria:

- Product rules, supported formats, size limit, UI states, and out-of-scope boundaries are documented.
- Requirements do not introduce persistence, queueing, or real AI work.

Validation:

- Atlas confirms the card is actionable.
- Ada confirms the scope fits the current architecture.

### SS2-002: Confirm Upload Architecture and Contract

Agent Owner: Ada
Supporting: Turing, Pixel
Status: Ready
Dependency: SS2-001

Value:

Frontend and backend need a simple upload contract that can evolve into object storage later.

Acceptance Criteria:

- Define a multipart upload endpoint and response shape.
- Preserve existing job and artifact response fields.
- Confirm that uploaded bytes are validated and discarded after request handling.
- Document contract changes in `packages/contracts`.

Validation:

- Contract schema parses successfully.
- Backend and frontend types remain aligned.

### SS2-003: Implement Multipart Audio Upload API

Agent Owner: Turing
Supporting: Ada
Status: Ready
Dependency: SS2-002

Value:

harmonIA needs to accept a real local audio file before the processing pipeline can become real.

Acceptance Criteria:

- Add a FastAPI multipart upload endpoint.
- Accept `.wav`, `.mp3`, and `.flac` files up to 100 MB.
- Reject unsupported extensions, empty files, and oversized uploads with clear errors.
- Create an in-memory queued job using the uploaded filename.
- Keep existing job retrieval routes stable.
- Add unit tests for changed backend code.

Validation:

- Backend and worker tests pass.
- Python compile checks pass.

### SS2-004: Add Desktop Audio Selection and Drag-and-Drop

Agent Owner: Pixel
Supporting: Maestro
Status: Ready
Dependency: SS2-001

Value:

Producers and musicians need a natural desktop interaction for choosing an audio file.

Acceptance Criteria:

- User can select a local audio file through a file picker.
- User can drag and drop a local audio file.
- UI shows the selected filename.
- Selecting a different file replaces the current selection.
- Unsupported files receive a clear validation message.
- Add unit tests for changed frontend code.

Validation:

- Desktop tests and build pass.
- Browser smoke confirms selection states where practical.

### SS2-005: Connect Desktop Upload to API Client

Agent Owner: Pixel
Supporting: Turing, Ada
Status: Ready
Dependency: SS2-003, SS2-004

Value:

The selected audio file must create a visible analysis job through the backend.

Acceptance Criteria:

- Add an isolated multipart upload function to the desktop API client.
- Submit only after the user starts analysis.
- Preserve loading and repeated-click prevention.
- Render returned job ID, status, source filename, and mocked artifacts.
- Render friendly API and connection errors.
- Add unit tests for changed frontend code.

Validation:

- Desktop tests and build pass.
- Browser smoke confirms Desktop -> Upload API -> queued job flow.

### SS2-006: Expand Backend Upload Tests

Agent Owner: Turing
Supporting: Grace
Status: Ready
Dependency: SS2-003

Value:

Upload validation must remain predictable before storage and real processing are introduced.

Acceptance Criteria:

- Test accepted `.wav`, `.mp3`, and `.flac` uploads.
- Test unsupported extension rejection.
- Test empty file rejection.
- Test oversized file rejection.
- Test returned source filename and mocked artifacts.
- Keep tests deterministic and independent of external services.

Validation:

- Backend and worker tests pass.

### SS2-007: QA Review and Regression Coverage

Agent Owner: Grace
Supporting: Turing, Pixel, Maestro
Status: Ready
Dependency: SS2-003, SS2-004, SS2-005, SS2-006

Value:

The first real ingestion loop needs coverage for both happy paths and validation failures.

Acceptance Criteria:

- Review backend and frontend developer unit tests.
- Add regression coverage for risky upload paths.
- Confirm existing mocked job retrieval behavior remains stable.
- Document manual smoke checks and known gaps.

Validation:

- Desktop tests, build, backend/worker tests, and browser smoke pass.

### SS2-008: Release v0.3.0

Agent Owner: Linus
Supporting: Atlas, Grace, Ada, Maestro
Status: Ready
Dependency: SS2-001 through SS2-007

Value:

The team needs a tested checkpoint after the first real local audio ingestion loop.

Acceptance Criteria:

- Confirm product scope with Maestro.
- Confirm technical readiness with Ada.
- Run the full validation suite.
- Prepare release notes.
- Tag `v0.3.0` only after tests pass and user approval is given.
- Document known limitations and rollback suggestion criteria.

Validation:

- `npm audit`
- `npm run desktop:build`
- `npm run desktop:test`
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests`
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai`
- Browser smoke for the upload flow.

## Sprint Risks

- Multipart uploads can consume memory if the backend validation is not bounded carefully.
- Browser smoke cannot fully represent native Tauri drag-and-drop behavior.
- Discarding uploaded bytes is intentional but temporary.
- Expanding scope into storage, queueing, or AI processing would put the sprint objective at risk.

## Definition of Done

- Maestro confirms the central objective is met.
- Ada confirms architecture stayed within scope.
- Atlas confirms all cards are complete or explicitly deferred.
- Grace confirms developer tests were reviewed.
- Validation commands pass.
- Linus confirms whether `v0.3.0` is ready to tag.
