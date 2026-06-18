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
Status: Done
Dependency: SS2-001

Value:

Frontend and backend need a simple upload contract that can evolve into object storage later.

Architecture Decision:

- Add `POST /v1/jobs/upload` as the Sprint 02 multipart endpoint.
- Accept `multipart/form-data` with one binary file part named `file`.
- Keep `POST /v1/jobs` for the existing mocked JSON job creation path.
- Return the existing `JobResponse` / `AnalysisJob` shape used by the desktop app.
- Create an in-memory queued job with `source_type: "upload"` and `source_name` set to the uploaded filename.
- Validate uploaded bytes during request handling and discard them after the job is created.
- Document the upload request boundary in `packages/contracts/upload.schema.json`.

Validation Rules:

- Accept `.wav`, `.mp3`, and `.flac` filenames.
- Reject unsupported extensions.
- Reject empty files.
- Reject files larger than 100 MB (`104857600` bytes).
- Return short, actionable validation errors.

Acceptance Criteria:

- Define a multipart upload endpoint and response shape. Done: `POST /v1/jobs/upload` returns the existing `AnalysisJob`.
- Preserve existing job and artifact response fields. Done: `job.schema.json` remains the response contract.
- Confirm that uploaded bytes are validated and discarded after request handling. Done for Sprint 02 architecture.
- Document contract changes in `packages/contracts`. Done: `upload.schema.json` and contracts README.

Validation:

- Contract schema parses successfully.
- Backend and frontend types remain aligned.

Handoff:

```text
Agent: Ada (Engineering Manager)
Scope: SS2-002 upload architecture and contract.
Changed: Added the multipart upload endpoint decision, validation rules, shared upload request schema, and architecture notes.
Validated: Contract schema parsing required; implementation tests remain in SS2-003 through SS2-007.
Risks: Backend must bound multipart reads carefully so oversized uploads do not consume unbounded memory.
Next: Turing can implement SS2-003 and SS2-006; Pixel can implement SS2-004 after product UI states are confirmed and SS2-005 after the API endpoint lands.
```

### SS2-003: Implement Multipart Audio Upload API

Agent Owner: Turing
Supporting: Ada
Status: Done
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

Implementation Notes:

- Added `POST /v1/jobs/upload` to the FastAPI jobs router.
- Added chunked upload byte validation with the Sprint 02 100 MB limit.
- Added filename extension, empty-file, and oversized-file rejection.
- Added the minimal `python-multipart` parser dependency required by FastAPI upload handling.

Handoff:

```text
Agent: Turing (Backend Developer)
Scope: SS2-003 multipart audio upload API.
Changed: Implemented the upload endpoint, validation helpers, and queued in-memory job creation using the uploaded filename.
Validated: `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` passed with 16 tests; `.venv\Scripts\python.exe -m compileall apps\api workers\ai` passed.
Risks: Request parsing still depends on FastAPI/Starlette multipart behavior; future storage work should add stronger streaming/storage boundaries.
Next: Pixel can wire the desktop client after SS2-004 selection and drag-and-drop behavior lands.
```

### SS2-004: Add Desktop Audio Selection and Drag-and-Drop

Agent Owner: Pixel
Supporting: Maestro
Status: Done
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

Implementation Notes:

- Added a hidden desktop file input triggered by the existing `Select file` action.
- Added drag-and-drop handling through the audio import area.
- Added frontend validation for supported extensions and empty files.
- Added selected-file rendering that replaces prior selections before submission.

Handoff:

```text
Agent: Pixel (Front-End Developer)
Scope: SS2-004 desktop audio selection and drag-and-drop.
Changed: Implemented file selection, drag-and-drop, selected filename display, and frontend validation states.
Validated: `npm run desktop:test` passed with 18 tests; `npm run desktop:build` passed; browser smoke confirmed the page loads and no-file validation is visible.
Risks: Browser smoke cannot fully automate native file-picker selection in the current in-app browser tool, so file selection is covered by React tests.
Next: Grace can review frontend unit tests during SS2-007.
```

### SS2-005: Connect Desktop Upload to API Client

Agent Owner: Pixel
Supporting: Turing, Ada
Status: Done
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

Implementation Notes:

- Added `uploadAudioJob(file)` to the isolated desktop API client.
- Submits multipart form data to `POST /v1/jobs/upload` only after the user starts analysis.
- Reused the existing loading, error, repeated-click prevention, and artifact rendering behavior.
- Preserved the older JSON `createJob` client for the v0.2 mocked flow and compatibility tests.

Handoff:

```text
Agent: Pixel (Front-End Developer)
Scope: SS2-005 desktop upload API integration.
Changed: Connected Run analysis to the selected local audio file and multipart upload client.
Validated: `npm run desktop:test` passed with 18 tests; `npm run desktop:build` passed; live multipart API smoke returned a queued job for `smoke.wav`.
Risks: Full browser-level file picker automation remains manual until the tool surface supports safe file selection.
Next: Grace can review coverage and document remaining manual smoke gaps in SS2-007.
```

### SS2-006: Expand Backend Upload Tests

Agent Owner: Turing
Supporting: Grace
Status: Done
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

Implementation Notes:

- Added accepted upload coverage for `.wav`, `.mp3`, and `.flac`.
- Added rejection coverage for unsupported extension, empty file, and oversized file.
- Confirmed returned upload jobs keep the expected source filename, queued status, and mocked artifacts.

Handoff:

```text
Agent: Turing (Backend Developer)
Scope: SS2-006 backend upload test expansion.
Changed: Added deterministic FastAPI TestClient coverage for upload success and validation failures.
Validated: Backend and worker tests passed with 16 total tests.
Risks: QA should still review whether manual browser/API smoke should cover multipart CORS and native desktop file submission.
Next: Grace can review backend tests during SS2-007 after frontend upload coverage is added.
```

### SS2-007: QA Review and Regression Coverage

Agent Owner: Grace
Supporting: Turing, Pixel, Maestro
Status: Done
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

QA Report:

- See `docs/sprints/sprint-02-qa-report.md`.

Handoff:

```text
Agent: Grace (QA)
Scope: SS2-007 Sprint 02 upload QA review and regression coverage.
Changed: Added upload CORS regression coverage and documented automated/manual QA results.
Validated: npm audit, desktop tests, desktop build, backend/worker tests, Python compile, browser smoke, and live multipart API smoke passed.
Risks: Native file-picker and Tauri drag-and-drop remain manual checks outside the current browser automation surface.
Next: Linus can prepare the v0.3.0 release review and request user approval before tagging.
```

### SS2-008: Release v0.3.0

Agent Owner: Linus
Supporting: Atlas, Grace, Ada, Maestro
Status: Done
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

Release Review:

- Release notes prepared in `docs/releases/v0.3.0.md`.
- Validation gates passed after `npm audit fix` updated Vite to clear a high-severity advisory.
- User approved release on 2026-06-18.
- Version metadata was bumped to `0.3.0`.
- Native Tauri build was attempted as an extra check and timed out after 10 minutes; no installer artifacts are included in this release checkpoint.

Handoff:

```text
Agent: Linus (Release Coordinator)
Scope: SS2-008 v0.3.0 release review.
Changed: Prepared release notes, bumped release metadata, recorded validation results, known limitations, and rollback suggestion criteria.
Validated: npm audit, desktop build, desktop tests, backend/worker tests, Python compile, schema parsing, browser smoke, and live multipart API smoke passed.
Risks: Native Tauri installer build timed out; native upload interactions remain manual; upload persistence and real processing are deferred.
Next: Commit and tag `v0.3.0`.
```

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
