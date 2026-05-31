# Sprint 01 QA Report: SS-007

Date: 2026-05-30
Release target: `v0.2.0`
Owner: QA

## Reviewed Scope

- API CORS configuration for `http://localhost:1420` and `http://127.0.0.1:1420`.
- API mocked job flow: `POST /v1/jobs`, `GET /v1/jobs/{job_id}`, artifacts endpoint, and missing-job `404` behavior.
- Desktop API client: default and configured base URL, request payload, service errors, network errors, and invalid JSON responses.
- Desktop UI: initial state, successful job rendering, artifacts, friendly error rendering, loading state, and repeated-click prevention.

## QA Additions

- Added an explicit backend assertion for the artifact fields consumed by the desktop flow.
- Added frontend API client coverage for an invalid JSON response from the service.

## Automated Coverage

| Area | Coverage |
| --- | --- |
| CORS | Allowed desktop origins pass preflight and receive response headers; an unlisted origin is rejected. |
| API routes | Job creation, job fetch, artifact fetch, and missing job `404` responses are covered. |
| API contract | Job fields and artifact field names used by the frontend are asserted. |
| Frontend API client | Default URL, environment override, trailing slash cleanup, payload, network error, rejected request, and invalid JSON response are covered. |
| Desktop UI | Initial, loading, repeated-click, success, artifact rendering, and error states are covered. |

## Validation Results

| Command | Result |
| --- | --- |
| `npm run desktop:test` | Passed after QA follow-up: 2 files, 10 tests. |
| `npm run desktop:build` | Passed. |
| `pytest --rootdir=. apps/api/tests workers/ai/tests` | Could not run directly because `pytest` is not available on `PATH`. |
| `.venv\Scripts\python.exe -m pytest --rootdir=. apps/api/tests workers/ai/tests` | Passed: 10 tests, with one pytest cache warning. |
| `git diff --check` | Passed. |
| `npm audit` | Passed: 0 vulnerabilities. |
| `npm --workspace apps/desktop run tauri -- build` | Passed: MSI and NSIS `v0.2.0` bundles generated. |

## Manual Smoke Checks

Completed:

1. Started the FastAPI API and Vite desktop shell locally.
2. Opened `http://localhost:1420`, clicked `Run analysis`, and confirmed the visible job ID, queued status, `demo.wav`, and five returned artifacts.
3. Confirmed the browser console had no warnings or errors after the successful Desktop -> API flow.
4. Confirmed the UI recovered after restarting the API and running the flow again.

Automated coverage used instead of a manual sandbox check:

1. Loading state and repeated-click prevention are covered by frontend unit tests.
2. Friendly offline service error is covered by frontend API client and UI tests.
3. A manual API-offline browser check could not complete because the sandbox denied terminating the spawned Uvicorn child process.

## Risks

- Jobs remain in memory and disappear when the API process restarts.
- The flow uses the mocked source name `demo.wav`; upload behavior is not part of this sprint.
- Browser-level desktop-to-API success and recovery integration were manually checked.
- The previous job is cleared when a new analysis starts. A regression test covers a failed retry after a successful request.
- Pytest reports a cache warning because `.pytest_cache\v\cache` could not be created over an existing filesystem entry.

## Handoff

Agent: QA
Scope: SS-007 review and regression coverage for Sprint 01 `v0.2.0`.
Changed: Backend artifact contract assertion, frontend invalid JSON client test, and this QA report.
Validated: Desktop tests, desktop build, backend/worker tests through `.venv`, and diff whitespace check passed.
Risks: The manual API-offline browser check could not terminate the spawned Uvicorn child process inside the sandbox; automated coverage passed.
Next: Release Coordinator can recommend `v0.2.0` for user approval, commit, tag, and push.
