# Sprint 01: v0.2.0 Desktop -> API Flow

## Sprint Summary

Duration: 15 calendar days
Planned start: 2026-05-30
Planned end: 2026-06-13
Release target: `v0.2.0`
Sprint owner: Product Manager (PM)
Delivery coordinator: Agent Manager

## Central Objective

Transform harmonIA from a static desktop shell into the first usable product loop: the desktop app must create an analysis job through the FastAPI backend and show the returned job state and expected artifacts in the interface.

This sprint intentionally keeps the analysis mocked. The goal is to validate the product flow and integration path before adding real upload, storage, queueing, or AI processing.

## Success Metrics

Product success:

- User can click `Run analysis` and receive visible job feedback in the desktop UI.
- UI displays job ID, status, source name, and returned artifacts.
- UI has clear loading, success, and error states.
- The flow works locally with API at `127.0.0.1:8000` and desktop shell at `localhost:1420`.

Engineering success:

- `POST /v1/jobs` and `GET /v1/jobs/{job_id}` remain stable and tested.
- Frontend API client is isolated from React components.
- API contract fields used by the frontend are covered by tests.
- No real upload, Redis, PostgreSQL, storage, auth, or AI work leaks into this sprint.

Quality success:

- `npm audit` returns 0 vulnerabilities.
- `npm run desktop:build` passes.
- `npm run desktop:test` passes.
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` passes.
- QA reviews developer unit tests before release.

Release success:

- All implementation cards are complete or explicitly deferred.
- Native Tauri build is attempted and result is documented.
- Release Coordinator can recommend tagging `v0.2.0`.
- Rollback suggestion criteria are documented before release.

## PM Card Rules

The Product Manager owns card writing and card readiness.

Every sprint card must include:

- User or system value.
- Owner and supporting agents.
- In-scope and out-of-scope boundaries.
- Acceptance criteria.
- Validation method.
- Release impact.
- Current status.

Cards should be small enough to be completed and tested independently. If a card cannot be validated without another card, the dependency must be explicit.

## Sprint Ceremony Rhythm

Kickoff:

- PM confirms sprint objective and card scope.
- EM confirms architecture constraints.
- Agent Manager confirms owners and dependencies.

Async daily check:

- Each active agent reports `Done`, `Next`, and `Blocked`.
- Agent Manager updates card status.

Mid-sprint review:

- PM checks whether the central objective is still reachable.
- EM checks for scope creep.
- QA checks whether tests are keeping pace with implementation.

QA freeze:

- No new feature scope.
- Only fixes, tests, and release readiness work.

Release review:

- Release Coordinator runs validation.
- PM confirms product scope.
- EM confirms technical readiness.
- QA confirms coverage and known gaps.

## Scope

In:

- Mocked/in-memory job flow.
- API CORS support for the local desktop web shell.
- Frontend API client.
- Frontend job state rendering.
- Unit tests for changed backend/frontend code.
- QA review checklist for the sprint.
- Release notes for `v0.2.0`.

Out:

- Real audio upload.
- YouTube/Spotify ingestion.
- Real AI processing.
- Redis queue integration.
- PostgreSQL persistence.
- Authentication/licensing.
- Paid plan or monetization implementation.

## Agent Assignments

| Agent | Sprint Responsibility |
| --- | --- |
| Product Manager | Write/refine cards, define user behavior, acceptance criteria, and success metrics |
| Engineering Manager | Keep API/frontend/contracts simple and aligned |
| Agent Manager | Track ownership, dependencies, status, and handoffs |
| Backend Developer | Implement API changes and backend unit tests |
| Front-End Developer | Implement desktop flow and frontend unit tests |
| QA | Review tests and add regression/flow coverage |
| Release Coordinator | Validate release readiness and prepare `v0.2.0` notes |

## Card Status Legend

- Draft: PM is still shaping the card.
- Ready: Card can be picked up by the owning agent.
- In Progress: Implementation or validation is underway.
- In Review: QA/EM/PM review is underway.
- Done: Card meets acceptance criteria and validation.
- Blocked: Card cannot proceed without a decision or dependency.
- Deferred: Card intentionally moved out of sprint scope.

## Cards

### SS-001: Define v0.2.0 Product Requirements

Owner: Product Manager
Supporting: Agent Manager, Engineering Manager
Dependency: None

User/System Value:

The team needs a precise product target before implementation starts, so agents can work independently without redefining behavior while coding.

Task:

Define the exact user behavior for creating an analysis job from the desktop app.

In Scope:

- Button-driven mocked analysis flow.
- Loading, success, and error behavior.
- Job details visible after success.
- Explicit source name for mock flow.

Out of Scope:

- Real file upload.
- Real audio validation.
- Real job processing.

Acceptance Criteria:

- User can start an analysis from the current `Run analysis` button.
- For this sprint, the source can be a mock source name such as `demo.wav`.
- While the request is running, the button shows a loading state and cannot be clicked repeatedly.
- On success, the UI shows job ID, status, source name, and artifacts.
- On failure, the UI shows a short error message.
- Requirements are documented in this sprint file.

Validation:

- Agent Manager confirms requirements are actionable.
- Engineering Manager confirms the scope does not require storage, queue, or real upload.

Release Impact:

- Defines the product behavior included in `v0.2.0`.

Status: Done

### SS-002: Confirm API Contract for Jobs

Owner: Engineering Manager
Supporting: Product Manager, Backend Developer, Front-End Developer
Dependency: SS-001

User/System Value:

Frontend and backend need a shared contract so the desktop app can render job data reliably.

Task:

Confirm the job response fields used by frontend and backend.

In Scope:

- Existing job response shape.
- Existing artifact response shape.
- Contract alignment with tests.

Out of Scope:

- Versioned public API.
- Upload metadata.
- Authentication fields.

Acceptance Criteria:

- Keep `id`, `source_type`, `source_name`, `status`, `created_at`, `updated_at`, `error`, and `artifacts`.
- Keep artifact fields: `id`, `kind`, `name`, `status`, `uri`.
- Use the existing JSON schema as the contract reference.
- Contract matches the current API response.
- Frontend types can be derived from the same shape.
- Any contract changes are reflected in `packages/contracts/job.schema.json`.

Validation:

- JSON schema parses successfully.
- Backend tests assert the fields the frontend needs.

Release Impact:

- Reduces release risk for Desktop -> API integration.

Status: Done

### SS-003: Add CORS Support to API

Owner: Backend Developer
Supporting: Engineering Manager, QA
Dependency: SS-002

User/System Value:

The desktop web shell must be able to call the local API during development.

Task:

Allow the local desktop web shell to call the FastAPI app.

In Scope:

- Development CORS origins.
- CORS settings in API app startup.
- Test or smoke coverage where practical.

Out of Scope:

- Production domain policy.
- Auth/session cookies.
- Public API gateway rules.

Acceptance Criteria:

- Allow `http://localhost:1420` and `http://127.0.0.1:1420`.
- Keep CORS config explicit and development-friendly.
- Do not open wildcard origins unless the EM approves it.
- Frontend dev server can call `POST /v1/jobs`.

Validation:

- Backend unit/smoke test passes.
- `python -m compileall apps\api workers\ai` passes.

Release Impact:

- Enables local desktop integration for `v0.2.0`.

Status: Done

### SS-004: Create Desktop API Client

Owner: Front-End Developer
Supporting: Engineering Manager, QA
Dependency: SS-002

User/System Value:

The desktop app needs a stable client layer for backend calls instead of embedding request logic inside UI components.

Task:

Create a small frontend API client for job creation.

In Scope:

- Job types.
- `createJob` function.
- Base URL configuration.
- Friendly error handling.
- Unit tests for client behavior where practical.

Out of Scope:

- Upload client.
- Polling client.
- Auth headers.

Acceptance Criteria:

- Add a single function to create a job.
- Default API base URL to `http://127.0.0.1:8000`.
- Allow future override through environment config.
- Return typed job data to the React app.
- Surface friendly errors for failed requests.
- API client is isolated from React components.

Validation:

- `npm run desktop:test` passes.
- `npm run desktop:build` passes.

Release Impact:

- Creates the frontend integration layer for `v0.2.0`.

Status: Done

### SS-005: Connect Run Analysis Button

Owner: Front-End Developer
Supporting: Product Manager, QA
Dependency: SS-003, SS-004

User/System Value:

Users can perform the first visible action in harmonIA: creating an analysis job and seeing the returned result.

Task:

Connect `Run analysis` to the API client and render the returned job.

In Scope:

- Button click handler.
- Loading state.
- Success state.
- Error state.
- Returned artifact rendering.

Out of Scope:

- File picker behavior.
- Drag-and-drop upload behavior.
- Polling after job creation.
- Audio preview/download.

Acceptance Criteria:

- Button calls the API once per click.
- Button shows loading state while the request is in flight.
- Repeated clicks are prevented while loading.
- UI shows job ID, status, source name, and artifacts after success.
- UI shows an error message after failure.
- Existing visual structure stays professional and desktop-focused.
- The static artifact list is replaced or clearly tied to returned API data.

Validation:

- Frontend unit test covers successful job creation.
- Frontend unit test covers error state if practical.
- Browser/manual smoke test confirms the flow works against local API.

Release Impact:

- Main user-facing feature for `v0.2.0`.

Status: Done

### SS-006: Expand Backend Tests for Job Flow

Owner: Backend Developer
Supporting: QA
Dependency: SS-002

User/System Value:

The mocked backend flow must remain stable while the frontend starts depending on it.

Task:

Strengthen backend tests for the mocked job lifecycle.

In Scope:

- Job creation test.
- Job fetch test.
- Artifact list test.
- Missing job behavior.

Out of Scope:

- Database tests.
- Queue tests.
- Worker integration tests.

Acceptance Criteria:

- Test `POST /v1/jobs`.
- Test `GET /v1/jobs/{job_id}`.
- Test `GET /v1/jobs/{job_id}/artifacts`.
- Test 404 behavior for missing job IDs.
- Backend tests assert the fields used by the frontend.
- Tests are deterministic and do not require external services.

Validation:

- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` passes.

Release Impact:

- Lowers API regression risk for `v0.2.0`.

Status: Done

### SS-007: QA Review and Regression Coverage

Owner: QA
Supporting: Backend Developer, Front-End Developer, Product Manager
Dependency: SS-003, SS-004, SS-005, SS-006

User/System Value:

The sprint needs confidence that the first product loop behaves correctly and does not regress the project shell.

Task:

Review developer tests and add missing coverage for the sprint flow.

In Scope:

- Review backend tests for route behavior.
- Review frontend tests for UI behavior.
- Add regression coverage for loading/repeated click behavior if practical.
- Document manual smoke checks.

Out of Scope:

- Full end-to-end automation framework.
- Real Tauri window automation.
- Performance testing.

Acceptance Criteria:

- QA can explain what is covered and what remains manual.
- No sprint card ships without relevant test review.
- Known gaps are documented before release.

Validation:

- Frontend tests pass.
- Backend/worker tests pass.
- Manual flow is documented if browser smoke testing is used.

Release Impact:

- Required before `v0.2.0` can be recommended for release.

Status: Done

### SS-008: Release v0.2.0

Owner: Release Coordinator
Supporting: Agent Manager, QA, Engineering Manager, Product Manager
Dependency: SS-001 through SS-007

User/System Value:

The team needs a tested release checkpoint after the first integrated product loop.

Task:

Prepare and validate the `v0.2.0` release once implementation cards are complete.

In Scope:

- Release notes.
- Validation commands.
- Native Tauri build result.
- Tag recommendation.
- Rollback suggestion criteria.

Out of Scope:

- Automatic rollback.
- Publishing installers outside GitHub.
- App signing.

Acceptance Criteria:

- Confirm release scope with PM.
- Confirm technical readiness with EM.
- Run full validation commands.
- Prepare concise release notes.
- Tag `v0.2.0` only after tests pass and user approval is given.
- Native Tauri build is attempted and result documented.

Validation:

- `npm audit` passes.
- `npm run desktop:build` passes.
- `npm run desktop:test` passes.
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` passes.
- Release Coordinator handoff includes test results, risks, and rollback suggestion criteria.

Release Impact:

- Creates the `v0.2.0` release candidate.

Status: Done

### SS-009: Make the Native Desktop Distribution Reproducible

Owner: Engineering Manager
Supporting: Front-End Developer, QA, Release Coordinator
Dependency: SS-005

User/System Value:

The harmonIA desktop installer must be reproducible and validated on a clean Windows machine while connecting to the remote FastAPI backend.

Bug:

During local validation, process startup was affected by duplicated Windows `Path`/`PATH` environment keys after installing Rust. Distribution hardening deserves its own sprint after the connected product flow is more mature.

In Scope:

- Build reproducibility in CI Windows.
- Clean-machine installation smoke tests.
- API environment configuration.
- WebView2 installation strategy.
- Code-signing plan.
- Single-command local developer startup.

Out of Scope:

- Offline AI processing.
- Bundling Python/FastAPI as a local sidecar.
- Embedding real AI models.

Acceptance Criteria:

- Distribution cards are refined during Sprint 3 planning.
- Connected desktop architecture remains the default.
- Offline mode remains explicitly deferred.

Validation:

- Sprint 3 planning review.

Release Impact:

- Deferred to Sprint 3. Does not block `v0.2.0`.

Status: Deferred to Sprint 3

## Sprint Validation Commands

```powershell
npm audit
npm run desktop:build
npm run desktop:test
.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests
```

Native build:

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
$env:RUSTUP_HOME = "$PWD\.rustup"
npm --workspace apps/desktop run tauri -- build
```

## Sprint Risks

- The API is still in memory, so jobs disappear when the server restarts.
- The desktop flow will use a mock source name until real upload exists.
- Native Tauri build may be slow on a fresh Rust cache.
- Browser/API smoke tests require both API and Vite dev server running locally.
- If the sprint expands into upload or AI work, `v0.2.0` may miss the 15-day window.
- Distribution hardening is deferred to Sprint 3.

## Definition of Done

- PM confirms the central objective is met.
- EM confirms architecture stayed within scope.
- All Ready cards except release are implemented, done, or explicitly deferred.
- QA confirms developer tests were reviewed.
- Validation commands pass.
- Manual smoke test result is recorded.
- Repo is clean after commit.
- Release Coordinator confirms whether `v0.2.0` is ready to tag.
