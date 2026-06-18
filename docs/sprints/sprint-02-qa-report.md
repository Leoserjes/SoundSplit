# Sprint 02 QA Report: SS2-007

Date: 2026-06-18
Release target: `v0.3.0`
Owner: Grace - QA

## Reviewed Scope

- API upload contract for `POST /v1/jobs/upload`.
- API multipart validation for accepted extensions, unsupported extensions, empty files, oversized files, source filename, queued status, artifacts, and CORS.
- Desktop API client multipart submission, service validation messages, network errors, and invalid JSON responses.
- Desktop UI file selection, drag-and-drop, selected filename rendering, no-file validation, unsupported-file validation, empty-file validation, upload errors, success rendering, and repeated-click prevention.
- Existing mocked JSON job creation path remains covered for v0.2 compatibility.

## QA Additions

- Added backend CORS regression coverage for the new multipart upload endpoint.
- Confirmed upload validation tests avoid allocating a real 100 MB fixture by patching the limit inside the test.
- Documented the browser-level native file-picker automation gap.

## Automated Coverage

| Area | Coverage |
| --- | --- |
| API upload route | Accepted `.wav`, `.mp3`, and `.flac` uploads create queued jobs with mocked artifacts. |
| API validation | Unsupported extension, empty file, and oversized file rejection paths are covered. |
| API CORS | JSON job creation and multipart upload preflight/response headers are covered for local desktop origins. |
| Desktop API client | Multipart FormData submission, API validation messages, network error, and invalid JSON response are covered. |
| Desktop UI | Initial state, no-file validation, file picker selection, drag-and-drop selection, invalid/empty file validation, upload success, upload failure, retry clearing, and repeated-click prevention are covered. |
| Existing behavior | `POST /v1/jobs`, job fetch, artifact fetch, missing-job `404`, and JSON client behavior remain covered. |

## Validation Results

| Command | Result |
| --- | --- |
| `npm audit` | Passed after `npm audit fix`: 0 vulnerabilities. |
| `npm run desktop:test` | Passed: 2 files, 18 tests. |
| `npm run desktop:build` | Passed with Vite `8.0.16`. |
| `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` | Passed: 18 tests. |
| `.venv\Scripts\python.exe -m compileall apps\api workers\ai` | Passed. |
| `git diff --check` | Passed with line-ending normalization warnings only. |

## Manual Smoke Checks

Completed:

1. Started FastAPI locally at `http://127.0.0.1:8000`.
2. Started the Vite desktop shell at `http://localhost:1420`.
3. Opened the desktop shell in the in-app browser and confirmed the analysis workspace rendered.
4. Clicked `Run analysis` without a selected file and confirmed the visible validation message.
5. Confirmed the browser console had no errors after the smoke check.
6. Submitted an in-memory multipart `smoke.wav` payload to the live API and confirmed `201`, `status: "queued"`, `source_type: "upload"`, and `source_name: "smoke.wav"`.

Automated coverage used instead of manual browser file selection:

1. The current in-app browser tool does not expose a safe native file-picker setter.
2. File picker selection, drag-and-drop selection, and Desktop -> upload client behavior are covered by React unit tests.
3. Multipart API behavior is covered by backend tests and live API smoke.

## Risks

- Uploaded bytes are intentionally discarded after validation during Sprint 02.
- Jobs remain in memory and disappear when the API process restarts.
- Full native Tauri drag-and-drop remains a manual check outside browser automation.
- Vite was updated by `npm audit fix` to clear a high-severity advisory; release review should include the updated lockfile.
- `npm audit fix` reported a non-blocking cleanup warning because the running Vite dev server held a Rolldown binding file open.

## Handoff

```text
Agent: Grace (QA)
Scope: SS2-007 review and regression coverage for Sprint 02 local audio upload.
Changed: Added upload CORS regression coverage and this QA report.
Validated: npm audit, desktop tests, desktop build, backend/worker tests, Python compile, browser smoke, and live multipart API smoke passed.
Risks: Native file-picker and Tauri drag-and-drop remain manual checks; uploaded bytes are not persisted by design.
Next: Linus can prepare the v0.3.0 release review and ask for user approval before tagging.
```
