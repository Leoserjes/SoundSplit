# Installer Permissions And Data Boundary Review

Status: Passed for Sprint 03 internal distribution review
GitHub Issue: `#16`
Owner: Ada - Engineering Manager
Supporting: Pixel - Front-End Developer, Grace - QA, Linus - Release Coordinator
Review Date: 2026-06-18

## Scope

This review covers the current harmonIA desktop installer and app data boundaries for the Sprint 03 connected upload workflow.

This review does not approve public distribution. Installer sharing remains internal-only until RLS3-003, clean-machine validation, and explicit user approval are complete.

## Evidence Reviewed

- `apps/desktop/src/App.tsx`
- `apps/desktop/src/App.test.tsx`
- `apps/desktop/src/api/config.ts`
- `apps/desktop/src/api/config.test.ts`
- `apps/desktop/src/api/jobs.ts`
- `apps/desktop/src/api/jobs.test.ts`
- `apps/desktop/src-tauri/Cargo.toml`
- `apps/desktop/src-tauri/src/main.rs`
- `apps/desktop/src-tauri/tauri.conf.json`
- `docs/sprints/sprint-03-release-artifact-safety-review.md`
- `docs/distribution/windows-diagnostic-build.md`
- `docs/distribution/webview2-strategy.md`
- Tauri v2 capability and permission docs

## Permission Surface

The current desktop app uses a minimal Tauri shell:

| Area | Current state | Review result |
| --- | --- | --- |
| Tauri native plugins | No `tauri-plugin-*` dependencies are declared in `Cargo.toml`. | No plugin-specific filesystem, dialog, shell, process, or HTTP permissions are requested. |
| Tauri commands | `main.rs` only initializes `tauri::Builder::default()` and runs the generated context. | No custom Rust commands expose native filesystem or OS access to the frontend. |
| Capability files | No `src-tauri/capabilities` directory is present. | No app-specific capability grants were found. |
| Frontend Tauri APIs | Source search found no `invoke`, filesystem, dialog, shell, path, process, or Tauri HTTP API usage. | The current upload flow does not use privileged Tauri IPC to read local files. |
| Browser file access | The app uses HTML file input and drag/drop `File` objects. | File access is limited to files selected or dropped by the user through WebView/browser behavior. |
| Installer runtime dependency | Windows uses WebView2 through Tauri; Sprint 03 keeps the default downloaded bootstrapper strategy. | WebView2 can require network during installation if missing, but this is a runtime dependency, not application data access. |

Tauri documentation describes capabilities as the boundary that grants windows and webviews access to Tauri core, app, or plugin commands. The current repo does not grant additional app/plugin permissions, and the frontend does not call privileged Tauri commands.

## File Selection And Upload Flow

The current UI has two supported file selection paths:

- A hidden `<input type="file">` opened by the `Select file` button.
- Drag and drop into the audio import area.

Both paths pass a single browser `File` object into `handleSelectedFile`. The app validates:

- extension is `.wav`, `.mp3`, or `.flac`;
- file size is greater than zero;
- file size is at most 100 MB.

Selecting or dropping a file does not submit it. The UI stores the selected `File` in React component state, clears any previous job result, and shows the selected filename. The file is submitted only when the user activates `Run analysis`.

The `Run analysis` handler blocks duplicate in-flight submissions, requires a selected file, and then calls `uploadAudioJob(selectedFile)`. The upload client appends that exact `File` as multipart field `file` and posts it to `/v1/jobs/upload`.

## Directory And Local Storage Boundaries

The desktop app does not currently read arbitrary directories:

- There is no directory picker.
- There is no `webkitdirectory` input.
- There is no recursive drag/drop traversal.
- Only `event.dataTransfer.files[0]` is read from a drop event.
- No native filesystem plugin or Rust file-reading command is exposed.

Current local storage behavior:

- Selected file metadata and the browser `File` reference are held in React memory only.
- Created job data is held in React memory only.
- Source search found no `localStorage`, `sessionStorage`, `indexedDB`, cookies, cache-storage calls, `FileReader`, or object URL creation in `apps/desktop/src`.
- The review found no app code that copies selected audio into app data directories before upload.

After upload starts, local file bytes cross the desktop boundary and are sent to the configured API. Backend retention, server-side processing, and remote artifact storage are outside this installer-permission review and should be covered by backend data-retention cards before wider testing.

## Network And API Target Behavior

The desktop app contacts the API through browser `fetch` calls:

| Operation | Endpoint | Payload |
| --- | --- | --- |
| Legacy typed job creation | `${getApiBaseUrl()}/v1/jobs` | JSON job request |
| Audio upload job creation | `${getApiBaseUrl()}/v1/jobs/upload` | Multipart form data with `file` |

The default API base URL is `http://127.0.0.1:8000`. Builds can override it through `VITE_API_BASE_URL`; the app trims trailing slashes and falls back to the default if the configured value is blank. `VITE_API_ENVIRONMENT` accepts `development`, `staging`, and `production`, defaulting to `development` for unknown values.

The Sprint 03 Windows diagnostic workflow sets `VITE_API_ENVIRONMENT=development` and `VITE_API_BASE_URL=http://127.0.0.1:8000`. The artifact safety review found no secret API target in the reviewed artifacts.

Current limitation: there is no runtime allow-list or CSP-level network policy documented for production. For Sprint 03 internal diagnostics this is acceptable because artifacts are not public and the expected API target is local, but production distribution should explicitly constrain API targets and CSP.

## Follow-Up Risks

- Add a future security-hardening card before public distribution to define CSP and API-target allow-list expectations for packaged builds.
- If future work adds Tauri plugins such as filesystem, dialog, shell, process, updater, or native HTTP, require an EM permission review and scoped capability file before implementation is accepted.
- Backend data-retention rules for uploaded audio are not covered by this desktop installer review and should be documented before non-developer tester workflows expand.
- Clean-machine install evidence remains blocked by SS3-004 until Windows Sandbox or a clean VM is available.

## Grace QA Review

Grace reviewed Ada's RLS3-002 permission and data-boundary review against the current desktop source, tests, Tauri shell, and sprint evidence. QA did not install the MSI or EXE on the host.

QA confirms the manual upload flow review passes for Sprint 03 internal distribution review:

- `App.tsx` uses a single browser `File` from either the file input or drag/drop, validates supported audio extensions, rejects empty files, enforces the 100 MB limit, and submits only after `Run analysis`.
- `jobs.ts` appends that same selected `File` to multipart field `file` and posts it to `/v1/jobs/upload`.
- `App.test.tsx` and `jobs.test.ts` cover selecting and uploading the exact file, dropped-file selection, no-file guard, validation failures, upload failure messaging, and duplicate-click blocking.
- `Cargo.toml`, `main.rs`, `tauri.conf.json`, and the missing `src-tauri/capabilities` directory match Ada's finding that no native plugins, custom commands, or app-specific capability grants are present.
- Source search found no browser persistence APIs, object URL creation, `FileReader`, directory upload, privileged Tauri IPC, or Tauri filesystem/dialog/shell usage in the reviewed desktop code.

Validation:

- `npm run desktop:test` passed with 25 tests across 3 files.
- `apps/desktop/src-tauri/tauri.conf.json` parsed as valid JSON.

Remaining QA caveats:

- This QA review validates the documented manual flow and code boundaries, not a clean-machine installer execution.
- SS3-004 remains the required clean VM/Sandbox installation gate.
- Production CSP/API target allow-listing and backend uploaded-audio retention remain follow-up risks before wider distribution.

## Result

RLS3-002 passes for Sprint 03 internal distribution review.

The current installer and desktop app do not request or expose broad local filesystem access beyond user-selected browser `File` objects. The app does not read arbitrary directories, does not persist selected audio locally in app code, and submits the selected file only when the user starts analysis. Network behavior is documented and remains internal-diagnostic until sharing gates are complete.

## References

- https://v2.tauri.app/security/capabilities/
- https://v2.tauri.app/security/permissions/
- https://v2.tauri.app/plugin/file-system/
- https://v2.tauri.app/reference/acl/capability/

## Handoff

```text
Agent: Ada (Engineering Manager)
Scope: RLS3-002 installer permissions and desktop data boundary review.
Changed: Added the installer permissions and data boundary review document; documented current Tauri permission surface, file-selection flow, local storage behavior, and API target behavior.
Validated: Reviewed desktop source/tests, Tauri config/Rust shell, release artifact safety review, Windows diagnostic workflow, WebView2 strategy, and Tauri permission/capability docs; searched for privileged Tauri APIs and browser persistence APIs; did not install MSI or EXE on the host.
Risks: Production CSP/API target allow-list is not defined; future Tauri plugins need scoped capabilities; backend uploaded-audio retention is outside this review; clean-machine install remains blocked until SS3-004 can run in a clean VM or Windows Sandbox.
Next: Main thread can review and update GitHub issue #16; Linus can proceed with RLS3-003 using this review as a sharing gate input.
```
