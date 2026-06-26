# Sprint 04: v0.5.0 Durable Jobs And Artifacts

Status: Draft

## Sprint Summary

Duration: 14 calendar days
Planned start: 2026-07-03
Planned end: 2026-07-17
Release target: `v0.5.0`
Sprint owner: Maestro - Product Manager
Delivery coordinator: Atlas - Agent Manager

## Central Objective

Move harmonIA from in-memory job state and discarded uploads to a durable job and artifact foundation. The sprint should preserve the connected desktop direction while adding persistent job metadata, a repository-owned file/artifact boundary, and desktop behavior that can refresh job status and expose downloadable artifacts.

This sprint is not about real AI processing. Mocked or placeholder artifacts are acceptable while the team proves the persistence, artifact, and desktop refresh flow that later worker and model sprints will reuse.

## Success Metrics

Product success:

- Uploaded audio is retained through an explicit storage boundary instead of being discarded after validation.
- A created job can survive an API process restart when persistent services are available.
- Users can refresh or revisit a job and see current status and artifact availability.
- Downloadable artifact metadata is clear even when artifacts are mocked.

Engineering success:

- Job and artifact state are accessed through repository/service boundaries instead of direct in-memory dictionaries.
- Persistence and file storage configuration are explicit and documented.
- Upload handling keeps the Sprint 02 validation rules while adding durable storage behavior.
- The architecture can evolve toward S3-compatible object storage without requiring hosted cloud services now.
- The implemented API surface is discoverable through an accurate OpenAPI schema and Swagger UI.

Quality success:

- Backend tests cover durable job creation, upload persistence, artifact listing, and missing-artifact behavior.
- Desktop tests cover status refresh and artifact action states.
- Data retention and local file safety are reviewed before release.
- Automated checks confirm the OpenAPI schema includes the expected routes and methods.

Release success:

- Release notes for `v0.5.0` identify the durable behavior and the remaining mocked processing limits.
- No real AI, queue, or model dependency is implied by the release.
- Rollback criteria cover persistence and artifact storage failures.

## Scope

In:

- Durable job metadata design and implementation.
- Artifact metadata design and implementation.
- Upload persistence after validation.
- Repository/service boundaries for jobs and artifacts.
- Local development storage boundary for retained uploads and generated/mock artifacts.
- Artifact listing and download behavior.
- API endpoint inventory, OpenAPI metadata, and Swagger UI documentation.
- Desktop job refresh/polling and artifact availability states.
- QA report and release notes for `v0.5.0`.

Out:

- Real stem separation.
- Audio normalization.
- Redis-backed queue execution.
- Production cloud object storage.
- Authentication, user accounts, or licensing.
- Offline AI processing.
- Public installer distribution.

## Product Rules

- Supported upload formats remain `.wav`, `.mp3`, and `.flac`.
- Maximum upload size remains 100 MB unless Maestro and Ada approve a change.
- The desktop app must only upload files after explicit user action.
- Stored uploads and artifacts must stay within an app-controlled data directory or configured storage boundary.
- Raw uploaded audio must not be bundled into release or installer artifacts.
- Jobs may still return mocked artifact outputs, but the UI must not imply real analysis has completed unless the backend state says so.

## Proposed Technical Decisions For Review

- Keep the API contract centered on `AnalysisJob` and artifact metadata.
- Introduce a job repository boundary before adding queue or worker execution.
- Prefer PostgreSQL for durable job metadata when local infrastructure is running, with clear test seams.
- Add a local filesystem artifact adapter for development and tests.
- Keep MinIO/S3-compatible object storage as a future implementation of the storage adapter unless EM approves pulling it into Sprint 04.
- Use environment configuration for storage roots and persistence behavior.

## Cards

### SS4-001: Confirm Durable Job And Artifact Architecture

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Ada
Supporting: Maestro, Turing, Pixel, Grace
Status: Draft
Dependency: Sprint 03 completion or explicit user approval

Value:

The team needs one agreed persistence and artifact boundary before backend and desktop work starts.

In Scope:

- Define job metadata fields that must persist.
- Define artifact metadata fields and download behavior.
- Decide the Sprint 04 storage adapter boundary.
- Document which services are required for local development and tests.
- Confirm what remains mocked until the worker pipeline sprint.

Out of Scope:

- Real AI processing.
- Queue implementation.
- Production cloud storage.

Acceptance Criteria:

- Architecture notes are added to `docs/architecture.md` or a linked sprint decision.
- Persistence, storage, and artifact responsibilities are explicit.
- EM and PM approve that the sprint remains durable-but-mocked.
- Follow-up cards are created for any deferred storage or database concerns.

Validation:

- Documentation review by Ada and Maestro.
- Atlas confirms implementation cards are actionable.

### SS4-009: Document API Surface With OpenAPI And Swagger

GitHub Issue: TBD after Sprint 04 approval
Agent Owner: Turing
Supporting: Ada, Pixel, Grace, Atlas
Status: Draft
Dependency: SS4-001; maintained as SS4-002 through SS4-005 add or change endpoints

Value:

Developers, frontend agents, QA, and future integrators need one reliable map of the implemented API rather than reconstructing routes from backend source files.

In Scope:

- Use FastAPI's generated OpenAPI schema as the API documentation source of truth.
- Keep interactive Swagger UI available at `/docs` and the machine-readable schema at `/openapi.json` for approved development/internal environments.
- Add API title, version, description, route tags, operation summaries, and response metadata.
- Document every implemented endpoint with method, path, purpose, request shape, response shape, status codes, and expected error cases.
- Group endpoints by domain, including health, jobs, uploads, and artifacts.
- Link shared schemas under `packages/contracts` where they define an API boundary.
- Document the current authentication state and clearly distinguish implemented endpoints from planned endpoints.
- Add a repository documentation page that links to Swagger UI and records how to export or inspect the OpenAPI schema.

Out of Scope:

- Publishing Swagger UI as a public production endpoint.
- Authentication implementation.
- Generating client SDKs.
- Documenting planned endpoints as if they already exist.

Acceptance Criteria:

- Swagger UI loads successfully at `/docs` in the approved development environment.
- `/openapi.json` returns valid OpenAPI JSON.
- Every implemented API route has a clear tag, summary, response model where applicable, and documented error responses.
- The endpoint inventory covers all currently registered harmonIA routes and is updated for Sprint 04 route changes.
- A backend test asserts that expected paths and methods are present in the generated OpenAPI schema.
- README or developer documentation links to the API reference.
- Grace confirms the documentation is sufficient to execute the Sprint 04 golden API flow without reading route source code.

Validation:

- FastAPI TestClient check for `GET /openapi.json`.
- Schema assertion for expected paths and HTTP methods.
- Manual Swagger UI smoke at `/docs`.
- Documentation review by Ada, Pixel, and Grace.

### SS4-002: Add Persistent Job Repository Baseline

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Turing
Supporting: Ada, Grace
Status: Draft
Dependency: SS4-001

Value:

Jobs should no longer disappear solely because the API process restarts when persistent infrastructure is available.

In Scope:

- Add a repository boundary for job creation, lookup, status updates, and artifact attachment.
- Add persistent job metadata storage according to the SS4-001 decision.
- Preserve current job response contracts.
- Keep tests deterministic and isolated.

Out of Scope:

- Worker queue execution.
- User-owned project/account tables.
- Production migration automation beyond the approved MVP baseline.

Acceptance Criteria:

- `POST /v1/jobs` and `POST /v1/jobs/upload` use the repository boundary.
- `GET /v1/jobs/{job_id}` returns persisted job metadata.
- Existing response fields remain compatible with `packages/contracts/job.schema.json`.
- Backend tests cover create and fetch behavior through the new repository.

Validation:

- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests`
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai`

### SS4-003: Persist Validated Uploads Through Storage Service

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Turing
Supporting: Ada, Grace
Status: Draft
Dependency: SS4-001, SS4-002

Value:

The next pipeline stages need access to uploaded audio through a controlled storage boundary.

In Scope:

- Add a storage service interface for uploaded source files.
- Persist validated upload bytes after Sprint 02 validation succeeds.
- Record source file metadata on the job.
- Keep uploaded files out of release artifacts and test caches.
- Add cleanup guidance for local development data.

Out of Scope:

- Streaming multipart directly to cloud storage.
- Model input preprocessing.
- Long-term retention policy beyond MVP guidance.

Acceptance Criteria:

- Accepted uploads are stored under the configured storage boundary.
- Rejected uploads are not retained.
- Stored file metadata is linked to the job.
- Tests cover accepted, rejected, and missing stored-file paths.
- Documentation explains where local uploads are stored and how to clean them.

Validation:

- Backend tests.
- Manual API smoke upload.
- Data directory inspection for expected file placement.

### SS4-004: Add Artifact Metadata And Download Boundary

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Turing
Supporting: Pixel, Ada, Grace
Status: Draft
Dependency: SS4-001, SS4-002, SS4-003

Value:

The desktop app needs real artifact availability semantics before the worker starts producing real outputs.

In Scope:

- Persist artifact metadata separately from transient mocked job construction.
- Add or refine artifact download route behavior.
- Represent pending, available, and failed artifact states.
- Use placeholder/mock artifact files only when clearly marked by backend state.
- Keep artifact response shape compatible with existing contracts or update contracts intentionally.

Out of Scope:

- Stem generation.
- MIDI/MusicXML generation.
- Signed download URLs for hosted storage.

Acceptance Criteria:

- `GET /v1/jobs/{job_id}/artifacts` reads from persisted artifact metadata.
- Download behavior is documented and tested.
- Missing job and missing artifact paths return clear errors.
- Contract schemas are updated if response fields change.

Validation:

- Backend tests.
- Contract schema parse check.
- Manual API smoke for artifact listing/download.

### SS4-005: Add Desktop Job Refresh And Artifact Actions

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Pixel
Supporting: Maestro, Turing, Grace
Status: Draft
Dependency: SS4-002, SS4-004

Value:

Users need the desktop app to reflect durable backend state instead of only showing the initial upload response.

In Scope:

- Add API client support for fetching a job by ID and listing artifacts.
- Add a lightweight refresh or polling behavior after job creation.
- Show artifact availability and download/open actions.
- Preserve friendly connection and validation errors from Sprint 03.
- Add frontend tests for refresh and artifact action states.

Out of Scope:

- Full project history UI.
- Authentication.
- Local file manager integration beyond safe artifact download/open behavior.

Acceptance Criteria:

- Desktop can refresh the active job state from the API.
- Artifact actions are disabled or explained when artifacts are pending/unavailable.
- API errors do not erase the last known job state.
- Frontend tests cover loading, success, unavailable, and error paths.

Validation:

- `npm run desktop:test`
- `npm run desktop:build`
- Browser/manual smoke where practical.

### SS4-006: Review Data Retention And Local File Safety

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Grace
Supporting: Ada, Linus
Status: Draft
Dependency: SS4-003, SS4-004

Value:

Persisting uploads changes the product risk profile and needs explicit safety review before release.

In Scope:

- Document what data is retained locally or in configured services.
- Confirm release artifacts do not include raw uploaded audio.
- Confirm local storage paths are not accidentally inside source-controlled or build-output directories.
- Confirm test fixtures and local data are excluded from packaging.
- Identify retention/deletion follow-up cards.

Out of Scope:

- Full privacy policy.
- Account-level data deletion.
- Formal security audit.

Acceptance Criteria:

- Data retention and local file safety notes are included in the Sprint 04 QA report.
- Any unsafe storage path blocks release or creates a required fix card.
- `.gitignore` or packaging exclusions are updated if needed.

Validation:

- Manual storage inspection.
- QA report.
- Release artifact exclusion review if installer diagnostics continue from Sprint 03.

### SS4-007: QA Review And Durable Flow Regression Coverage

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Grace
Supporting: Turing, Pixel, Ada, Linus
Status: Draft
Dependency: SS4-001 through SS4-006

Value:

Durable storage and artifact behavior can create regressions that unit tests alone may miss.

In Scope:

- Review backend and frontend developer tests.
- Add regression coverage for persistence, upload retention, artifact listing, and error states.
- Run manual API and desktop smoke checks.
- Document known gaps and release blockers.

Out of Scope:

- Full desktop E2E automation framework.
- Load testing.
- Production backup/restore testing.

Acceptance Criteria:

- Sprint 04 QA report is added under `docs/sprints/`.
- Validation command results are recorded.
- Manual smoke coverage and gaps are explicit.
- Release-safety implications are documented.

Validation:

- `npm audit`
- `npm run desktop:test`
- `npm run desktop:build`
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests`
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai`

### SS4-008: Release v0.5.0

GitHub Issue: TBD after Sprint 03 completion
Agent Owner: Linus
Supporting: Atlas, Grace, Ada, Maestro
Status: Draft
Dependency: SS4-001 through SS4-007

Value:

The team needs a tested checkpoint after durable job and artifact behavior lands.

In Scope:

- Prepare release notes for `v0.5.0`.
- Record validation results and known limitations.
- Confirm storage and retention safety review.
- Confirm no real AI processing is implied.
- Ask for user approval before tagging.

Out of Scope:

- Public installer distribution.
- Automatic rollback.
- Sharing stored user files or raw uploads.

Acceptance Criteria:

- Release notes are prepared.
- QA report is complete.
- Validation gates pass or blockers are documented.
- Rollback suggestion criteria include persistence and storage failures.
- User approval is received before tagging.

Validation:

- Full Sprint 04 validation suite.
- Release Coordinator review.

## Recommended Sequencing

1. SS4-001 confirms architecture and scope.
2. SS4-009 establishes the API/OpenAPI inventory and stays current as Sprint 04 routes change.
3. SS4-002 builds the persistent job repository baseline.
4. SS4-003 persists validated uploads through the storage service.
5. SS4-004 adds artifact metadata and download behavior.
6. SS4-005 updates the desktop refresh and artifact actions.
7. SS4-006 performs data retention and file safety review.
8. SS4-007 and SS4-008 close the sprint.

## Sprint Risks

- Persistence may introduce test flakiness if service boundaries are not isolated.
- Storing uploaded files increases local data safety responsibilities.
- Database and storage decisions can create rework if they skip the repository/adapter boundary.
- Desktop polling must remain lightweight and understandable.
- Installer diagnostics from Sprint 03 must not accidentally package local retained uploads.

## Definition Of Ready For Sprint Start

- Sprint 03 is complete or explicitly paused by the user.
- Maestro confirms product scope.
- Ada confirms persistence and storage constraints.
- Atlas creates or updates GitHub issue cards from this plan.
- Required local infrastructure and environment expectations are documented.

## Definition Of Done

- Approved cards are Done or explicitly Deferred.
- Durable job and artifact behavior is implemented or blockers are documented.
- API endpoints are mapped in the generated OpenAPI schema and reviewed through Swagger UI.
- QA report is complete.
- Release notes are prepared.
- User approves any release tag.
