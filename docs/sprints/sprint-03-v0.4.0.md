# Sprint 03: v0.4.0 Connected Desktop Distribution

Status: Open

## Sprint Summary

Duration: 14 calendar days
Planned start: 2026-06-18
Planned end: 2026-07-02
Release target: `v0.4.0`
Sprint owner: Maestro - Product Manager
Delivery coordinator: Atlas - Agent Manager

## Central Objective

Prepare harmonIA for reliable Windows distribution as a connected desktop app without treating installer output as production-ready yet. The desktop client remains a Tauri/React app that calls a FastAPI backend over HTTP. Sprint 03 should make configuration, local startup, installer build diagnostics, release-safety checks, and distribution decisions explicit before the project moves into broader internal testing.

This sprint is not about offline AI, local model packaging, production cloud deployment, or public installer distribution. Its goal is to make the connected desktop path reproducible, reviewable, and safe enough for an internal installer-readiness checkpoint.

## Review Notes

The team has two explicit review concerns before Sprint 03 starts:

- Installer timing: building final installer polish too early may create rework as the product changes. Sprint 03 therefore treats installer work as diagnostics, CI readiness, and internal validation rather than public distribution.
- Installer safety: no installer artifact should be shared externally until release-safety cards confirm that secrets, local files, uploaded audio, internal logs, and unintended configuration are not leaked.

## Success Metrics

Product success:

- The desktop app can clearly target local, staging, or production API environments.
- Users receive clear messaging when the connected API is unavailable.
- Internal testers have an understandable startup and distribution-readiness story.
- Distribution decisions are documented before installer behavior is treated as release policy.
- Release-safety checks reduce the risk of leaking secrets, user files, logs, or internal configuration through installer artifacts.

Engineering success:

- API base URL configuration has explicit precedence and tests.
- Local developer startup is available through one documented command.
- Windows installer CI is defined as diagnostic/internal readiness work or produces clear failure logs.
- WebView2 and code-signing decisions are documented without committing to paid services.
- Installer artifacts have an explicit safety review before they are shared outside the development team.
- Offline mode remains explicitly deferred.

Quality success:

- Frontend tests and build pass for configuration changes.
- Backend/worker tests remain green.
- CI build logs or internal artifacts are available for release review.
- Clean-machine validation has a repeatable checklist and explicit data-leak checks.
- Release-safety cards document what was checked and what remains unverified.
- Manual gaps are documented before release.

Release success:

- All implementation/planning cards are complete or explicitly deferred.
- Release notes for `v0.4.0` document distribution readiness and remaining limitations.
- Native installer artifacts are produced by CI for internal review only, or failure details are documented.
- Release-safety checks pass before any installer artifact is shared outside the core team.
- Rollback suggestion criteria are documented before release.

## Scope

In:

- Environment-aware API URL configuration.
- Clear offline/connection error handling.
- Single-command local developer startup.
- Windows CI workflow for desktop installer build diagnostics and internal artifacts.
- Clean-machine installation validation plan and results if artifacts are available.
- WebView2 installer strategy decision.
- Windows code-signing plan.
- Release-safety checks for secrets, local files, environment variables, logs, permissions, artifact integrity, and sharing policy.
- Release notes for `v0.4.0`.

Out:

- Offline AI processing.
- Local PyTorch model distribution.
- Python/FastAPI sidecar packaging.
- Automatic model downloads.
- Purchasing certificates or other paid services.
- Production cloud API deployment.
- Public installer distribution.
- Production-ready installer publishing.
- App store distribution.
- YouTube or Spotify ingestion.

## Product Rules

- harmonIA remains a connected desktop app.
- Local development should continue to default to `http://127.0.0.1:8000`.
- Staging and production API URLs may be placeholders until a hosted backend exists.
- The desktop app must fail gracefully when the API is unavailable.
- Installer and release decisions must not imply offline functionality.
- Paid distribution choices require explicit EM and PM approval before purchase or implementation.
- Installer artifacts are internal-only until release-safety checks pass and the user explicitly approves sharing.
- Release artifacts must not include `.env` files, credentials, local user files, raw uploaded audio, development logs with secrets, or private machine paths beyond unavoidable build metadata.
- Native installer work should minimize rework by focusing first on diagnostics, configuration, and safety policy before final packaging polish.

## Proposed Technical Decisions For Review

- API URL precedence:
  1. `VITE_API_BASE_URL` when set for the desktop web shell/build.
  2. Default local development URL: `http://127.0.0.1:8000`.
- Environment names:
  - `development`
  - `staging`
  - `production`
- Startup command:
  - Prefer a small repository-owned Node script over adding a process-manager dependency.
- CI:
  - Start with Windows diagnostic build and artifact upload.
  - Treat a clear build failure log as acceptable first CI output if installer creation still needs platform work.
- Installer maturity:
  - Treat Sprint 03 installer artifacts as internal diagnostics unless release-safety cards pass.
  - Do not market or publish installer artifacts as production-ready in this sprint.
- WebView2:
  - Decide documented default before treating installer output as release-ready.
- Code signing:
  - Planning only in Sprint 03.

## Card Readiness Legend

- Draft: Needs review before implementation.
- Ready: Can be picked up by the owning agent.
- In Progress: Implementation or validation is underway.
- In Review: QA/EM/PM review is underway.
- Done: Meets acceptance criteria and validation.
- Blocked: Cannot proceed without a decision or dependency.
- Deferred: Intentionally moved out of sprint scope.

## Cards

### SS3-001: Add Environment-Aware API Configuration

GitHub Issue: `#1`
Agent Owner: Pixel
Supporting: Ada, Grace
Status: Done
Dependency: Sprint 03 approval

Value:

The connected desktop app needs a clear API target model before distribution can be tested across local, staging, and production contexts.

In Scope:

- Keep `VITE_API_BASE_URL` as the desktop API base URL override.
- Document local, staging, and production API URL behavior.
- Preserve local default: `http://127.0.0.1:8000`.
- Add or update `.env.example` with desktop API URL guidance.
- Keep request code isolated in the desktop API client.
- Improve friendly connection/offline messaging where needed.
- Add frontend tests for configuration precedence and error messaging.

Out of Scope:

- Deploying a staging or production API.
- Authentication or licensing.
- Offline mode.
- Local FastAPI sidecar packaging.

Acceptance Criteria:

- Desktop API URL precedence is documented.
- Local development works without any extra environment variable.
- A configured `VITE_API_BASE_URL` is used without retaining trailing slashes.
- API connection failure messaging is short and actionable.
- Frontend tests cover default and configured API URL behavior.
- Desktop build and tests pass.

Validation:

- `npm run desktop:test`
- `npm run desktop:build`
- Browser/manual smoke for offline API messaging where practical.

Release Impact:

- Required before distribution testing can meaningfully represent connected desktop behavior.

Implementation Notes:

- Added a dedicated desktop API configuration module for `VITE_API_BASE_URL` and `VITE_API_ENVIRONMENT`.
- Preserved the default local API target: `http://127.0.0.1:8000`.
- Added explicit supported environment names: `development`, `staging`, and `production`.
- Normalized configured API URLs by trimming whitespace and trailing slashes.
- Updated the desktop connection failure message to tell testers to check that the API is running.
- Documented desktop API configuration in `.env.example` and `README.md`.
- Added focused frontend tests for API URL precedence, blank fallback, and environment names.

Validation Result:

- `npm run desktop:test` passed with 25 tests across 3 files.
- `npm run desktop:build` passed.
- Browser smoke was not run because this card changed API configuration and copy only, with coverage in frontend tests.

Handoff:

```text
Agent: Pixel (Front-End Developer)
Scope: SS3-001 environment-aware API configuration.
Changed: Added typed desktop API config helpers, documented Vite API environment variables, preserved the local default API URL, and improved the unreachable-service message.
Validated: npm run desktop:test passed with 25 tests; npm run desktop:build passed.
Risks: Staging and production API URLs remain placeholders until hosted API environments exist.
Next: Ada can start SS3-002 single-command startup with the API target behavior now documented.
```

### SS3-002: Create Single-Command Developer Startup

GitHub Issue: `#2`
Agent Owner: Ada
Supporting: Turing, Pixel, Grace
Status: Done
Dependency: Sprint 03 approval

Value:

Developers and testers need one reliable command to start the local FastAPI service and desktop web shell without fragile shell-specific setup.

In Scope:

- Add a repository-owned startup command for local development.
- Start FastAPI and the desktop dev shell together.
- Keep Rust setup separate from normal startup.
- Document logs, ports, shutdown behavior, and prerequisites.
- Avoid relying on temporary `PATH` mutations for ordinary dev startup.

Out of Scope:

- Packaging Python as a desktop sidecar.
- Starting Redis, PostgreSQL, or object storage.
- Installing Rust automatically.
- Adding a paid or hosted service.

Acceptance Criteria:

- One documented command starts the API and desktop web shell.
- The command uses the existing `.venv` Python path and npm workspace scripts.
- The command exits child processes when stopped.
- Startup logs make API and desktop URLs visible.
- README or developer docs are updated.
- Existing separate commands still work.

Validation:

- Run the startup command locally.
- Confirm API health endpoint responds.
- Confirm desktop shell loads.
- `npm run desktop:test`
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests`

Release Impact:

- Reduces onboarding and release validation friction.

Implementation Notes:

- Added `npm run dev` as the repository-owned single-command startup.
- Added `scripts/dev-start.mjs` to start FastAPI and the desktop Vite shell together.
- The API uses the repository `.venv` Python path directly.
- The desktop process uses the existing `apps/desktop` npm workspace script.
- Startup logs print the API and desktop URLs and the `Ctrl+C` shutdown instruction.
- Added Windows child-process handling for duplicated `Path`/`PATH` variables.
- Added Windows-safe npm invocation through `cmd.exe /d /s /c npm`.
- Added `npm run dev:check` with Node built-in tests for the startup helper.
- Updated `README.md` with combined and separate startup commands.

Validation Result:

- `npm run dev:check` passed with 5 tests.
- `npm run dev` startup smoke confirmed API `/health` at `http://127.0.0.1:8000`.
- `npm run dev` startup smoke confirmed the desktop shell at `http://127.0.0.1:1420`.
- `npm run desktop:test` passed with 25 tests across 3 files.
- `npm run desktop:build` passed.
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` passed with 18 tests.
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai` passed.

Handoff:

```text
Agent: Ada (Engineering Manager)
Scope: SS3-002 single-command developer startup.
Changed: Added npm run dev, repository-owned process orchestration, startup helper tests, README usage docs, and Windows-safe child process handling.
Validated: npm run dev:check; npm run dev smoke for API health and desktop shell; npm run desktop:test; npm run desktop:build; backend/worker pytest; Python compileall.
Risks: The smoke cleanup uses forced process-tree termination in automation; normal interactive Ctrl+C remains the intended developer shutdown path.
Next: Linus and Ada can use this startup path while working on SS3-005/SS3-003 distribution diagnostics.
```

### SS3-005: Decide WebView2 Strategy

GitHub Issue: `#5`
Agent Owner: Ada
Supporting: Maestro, Linus
Status: Done
Dependency: Sprint 03 approval

Value:

Windows installer behavior depends on how harmonIA handles WebView2 availability. The team needs a documented default before clean-machine validation becomes release policy.

In Scope:

- Compare WebView2 downloaded bootstrapper, embedded bootstrapper, and offline installer modes.
- Document installer size, network requirement, user experience, and maintenance trade-offs.
- Recommend a default for internal testing.
- Call out when the decision should be revisited.

Out of Scope:

- Implementing unrelated installer changes.
- App store packaging.
- Enterprise deployment policy.
- Paid signing decisions.

Acceptance Criteria:

- A WebView2 strategy document is created.
- The document compares the practical options.
- The recommended default is approved by PM and EM before implementation.
- Release notes identify the chosen strategy or state that it remains deferred.

Validation:

- Documentation review by Ada and Maestro.
- Linus confirms release impact and validation implications.

Release Impact:

- Blocks final clean-machine installer confidence, but does not block local source development.

Decision:

- Keep Tauri's default `downloadBootstrapper` WebView2 strategy for Sprint 03 internal diagnostic builds.
- Do not add `bundle.windows.webviewInstallMode` to `tauri.conf.json` in this sprint because the current implicit default already matches the decision.
- Treat clean-machine installs without WebView2 and without internet as a documented distribution limitation, not as a connected-app runtime failure.

Implementation Notes:

- Added `docs/distribution/webview2-strategy.md`.
- Compared downloaded bootstrapper, embedded bootstrapper, offline installer, fixed runtime, and skip modes.
- Recommended the downloaded Evergreen bootstrapper for Sprint 03 to keep artifacts small and avoid premature offline packaging work.
- Documented clean-machine validation notes and release-note language for `v0.4.0`.

Validation Result:

- Reviewed current `apps/desktop/src-tauri/tauri.conf.json`.
- Parsed current Tauri config with PowerShell JSON conversion.
- Verified the strategy against current Tauri v2 and Microsoft WebView2 distribution documentation.

Handoff:

```text
Agent: Ada (Engineering Manager)
Scope: SS3-005 WebView2 strategy decision.
Changed: Documented the Sprint 03 WebView2 installation strategy and clean-machine validation expectations.
Validated: Tauri config parsed successfully; current Tauri/Microsoft WebView2 docs reviewed.
Risks: Clean machines without WebView2 may need internet during installation; offline installer mode remains deferred.
Next: Linus can use this decision in SS3-003 Windows CI build diagnostics, and Grace can use it for SS3-004 clean-machine validation.
```

### SS3-003: Add Windows CI Build

GitHub Issue: `#3`
Agent Owner: Linus
Supporting: Ada, Pixel, Grace
Status: Done
Dependency: SS3-005 preferred before final installer expectations

Value:

The release team needs a clean Windows build signal for frontend, backend, Rust/Tauri, and installer readiness without prematurely treating installer output as production-ready.

In Scope:

- Add a Windows GitHub Actions workflow for diagnostic/internal release readiness.
- Run npm audit, desktop tests, desktop build, Python tests, and Python compile.
- Attempt native Tauri build on Windows.
- Upload installer artifacts when produced, marked as internal review artifacts.
- Upload logs or diagnostic artifacts when native build fails.
- Document any secrets or permissions required.

Out of Scope:

- Automatic production publishing.
- Code signing.
- Paid build services.
- Deployment to an app store.

Acceptance Criteria:

- Workflow exists under `.github/workflows/`.
- Workflow can be triggered manually.
- Workflow runs validation gates before native packaging.
- MSI/NSIS artifacts are uploaded as internal review artifacts when build succeeds.
- If native build fails or times out, logs clearly identify the failing step.
- Workflow does not package `.env` files, local audio files, test outputs, or unrelated workspace files.
- CI result is documented in Sprint 03 QA/release notes.

Validation:

- Run workflow manually or document why it cannot run.
- Review uploaded artifacts or failure logs.
- Confirm local validation still passes.

Release Impact:

- Required before claiming reproducible Windows installer readiness. Does not by itself approve public installer sharing.

Implementation Notes:

- Added `.github/workflows/windows-diagnostic-build.yml`.
- Added manual `workflow_dispatch` support and push triggers for distribution-relevant files.
- Added Windows validation gates before native packaging.
- Added a native Tauri build attempt after validation gates pass.
- Uploaded MSI/EXE bundle outputs as short-retention internal diagnostic artifacts when build succeeds.
- Uploaded diagnostic logs and build manifests on both success and failure.
- Documented workflow purpose, triggers, permissions, and artifact policy in `docs/distribution/windows-diagnostic-build.md`.
- Removed the sprint plan document from workflow push paths so CI evidence updates do not retrigger native installer builds.

Validation Result:

- Workflow syntax was reviewed against GitHub Actions and Tauri guidance.
- `Get-Content .github\workflows\windows-diagnostic-build.yml` reviewed locally.
- `Get-Content apps\desktop\src-tauri\tauri.conf.json | ConvertFrom-Json | Out-Null` passed locally.
- Remote workflow run `27737626166` passed on `master`.
- Successful artifacts were uploaded as `harmonIA-windows-internal-installers` and `harmonIA-windows-diagnostic-logs`.

Handoff:

```text
Agent: Linus (Release Coordinator)
Scope: SS3-003 Windows CI build diagnostics.
Changed: Added the Windows diagnostic GitHub Actions workflow and distribution documentation for internal artifacts and diagnostics.
Validated: Local workflow review and Tauri config parse passed; GitHub Actions run 27737626166 passed and uploaded internal installer plus diagnostic-log artifacts.
Risks: Artifacts remain internal-only until RLS3-001, RLS3-002, and RLS3-003 complete the safety and sharing checks.
Next: RLS3-001 can inspect any produced artifacts or diagnostic bundles; SS3-004 can use successful artifacts for clean-machine validation.
```

### SS3-004: Validate Clean-Machine Installation

GitHub Issue: `#4`
Agent Owner: Grace
Supporting: Linus, Pixel, Ada
Status: Blocked
Dependency: SS3-003

Value:

Internal testing requires confidence that harmonIA launches on a clean Windows machine without development dependencies and behaves clearly when connecting to the API.

In Scope:

- Create a clean-machine validation checklist.
- Test installer artifacts from CI if available.
- Use Windows Sandbox or a clean VM when practical.
- Confirm desktop launch without Node, npm, Python, or Rust installed.
- Document connected API behavior and offline/error behavior.
- Document screenshots or exact observed results where practical.
- Check that the installed app does not expose local source paths, bundled secrets, uploaded audio fixtures, or development-only configuration.

Out of Scope:

- Automatic rollback.
- App signing implementation.
- Production deployment.
- Offline AI execution.

Acceptance Criteria:

- Clean-machine checklist exists.
- Installer source and version are recorded.
- Launch behavior is documented.
- API connectivity behavior is documented.
- Data-leak and permission observations are documented.
- Known blockers and manual gaps are recorded.
- QA signs off or marks the card blocked with reasons.

Validation:

- Manual clean-machine test if CI artifacts exist.
- QA report added under `docs/sprints/`.

Release Impact:

- Required before recommending installer artifacts for non-developer testers.

QA Result:

- SS3-004 is blocked because a valid clean-machine install requires Windows Sandbox or a clean VM, and no usable clean environment is available in this workspace.
- Host installation was not performed.
- `C:\WINDOWS\System32\WindowsSandbox.exe` was not found.
- Querying the `Containers-DisposableClientVM` optional feature from the current session reported that elevation is required.
- The artifact source and repeatable MSI/NSIS validation checklist are documented in `docs/sprints/sprint-03-ss3-004-clean-machine-installation-qa.md`.
- Grace recommends keeping installer artifacts internal-only and not moving this card to release review until the checklist is executed in a clean environment.

Handoff:

```text
Agent: Grace (QA)
Scope: SS3-004 clean-machine installation validation.
Changed: Added a QA blocker result, artifact-source reference, and repeatable clean-machine validation checklist for MSI and NSIS artifacts.
Validated: Reviewed SS3-004 acceptance criteria, RLS3-001 artifact safety findings, WebView2 strategy, and local clean-environment availability; did not install MSI or EXE on the host machine.
Risks: No actual clean-machine install evidence exists yet; connected API success may need a staging API build or explicit clean-machine backend setup because current diagnostics target a local API URL.
Next: Run the checklist in Windows Sandbox or a clean VM, capture exact install/launch/API observations, then update this card with pass/fail evidence.
```

### SS3-006: Plan Windows Code Signing

GitHub Issue: `#6`
Agent Owner: Linus
Supporting: Ada, Maestro
Status: Done
Dependency: Sprint 03 approval

Value:

The team needs to understand certificate requirements, cost, and workflow impact before distributing installers beyond internal testing.

In Scope:

- Document Windows code-signing certificate options.
- Estimate cost ranges and renewal implications.
- Document CI/release workflow impact.
- Identify decision points for EM and PM approval.
- Keep signing implementation deferred until approval.

Out of Scope:

- Purchasing a certificate.
- Signing production installers.
- Adding paid services without approval.

Acceptance Criteria:

- Code-signing plan document is created.
- Cost and workflow trade-offs are documented.
- EM and PM approval requirement is explicit.
- Release notes state whether signing remains deferred.

Validation:

- Linus reviewed the plan against Microsoft, Azure Artifact Signing, Tauri, SignTool, and CA/B Forum documentation.
- The plan keeps Ada, Maestro, and user approval as required gates before any purchase, account setup, CI signing work, or secret changes.
- No signing implementation, paid service, certificate purchase, CI secret change, or workflow secret change was made.

Release Impact:

- Planning artifact only for `v0.4.0`; code signing remains deferred.
- Windows installer artifacts for `v0.4.0` remain unsigned internal diagnostics and must not be redistributed externally until signing, provenance, safety, and explicit approval gates are complete.

Planning Result:

- Created `docs/distribution/windows-code-signing-plan.md`.
- Recommended Sprint 03 decision: defer code signing for `v0.4.0`, do not purchase certificates or services now, do not add secrets now, and prefer Azure Artifact Signing as the first future candidate if eligibility and cost are approved.
- Kept Microsoft Store signing, traditional OV certificates, and EV certificates documented as alternatives.

Release Notes Language:

```text
Windows installer artifacts for v0.4.0 are unsigned internal diagnostics. Code signing is intentionally deferred while the team validates installer safety, clean-machine installation, WebView2 behavior, and release provenance. Windows SmartScreen or enterprise policy may warn or block unsigned artifacts. Do not redistribute these artifacts externally until a signing decision, release safety review, provenance record, and explicit approval are complete.
```

Handoff:

```text
Agent: Linus (Release Coordinator)
Scope: SS3-006 Windows code-signing planning for Sprint 03.
Changed: Added the Windows code-signing plan, option comparison, approval gates, no-secret policy, CI impact notes, and v0.4.0 release-note language.
Validated: Reviewed Microsoft, Tauri, Azure Artifact Signing, SignTool, and CA/B Forum documentation; confirmed no signing implementation, purchases, CI secret changes, or workflow secret changes were added.
Risks: Azure Artifact Signing eligibility, final pricing, identity validation lead time, SmartScreen reputation behavior, and traditional certificate private-key logistics still need approval-time verification.
Next: Keep v0.4.0 artifacts unsigned and internal-only; revisit signing when external distribution becomes a PM-approved release goal and EM/user approval exists for paid services and CI secret handling.
```

### RLS3-001: Release Artifact Safety Review

GitHub Issue: `#15`
Agent Owner: Linus
Supporting: Ada, Grace
Status: Done
Dependency: SS3-003

Value:

The team needs confidence that release artifacts do not leak secrets, local files, uploaded audio, development logs, or internal-only configuration.

In Scope:

- Define a release artifact safety checklist.
- Inspect CI artifact contents when artifacts are produced.
- Confirm `.env`, `.env.*`, local audio files, raw uploaded files, `.pytest_cache`, `tmp`, and development-only logs are excluded.
- Confirm bundled frontend config does not contain secrets.
- Confirm release notes clearly state artifact sharing status.
- Document findings in the Sprint 03 QA or release report.

Out of Scope:

- Formal third-party security audit.
- Code signing implementation.
- Production data privacy certification.

Acceptance Criteria:

- Artifact safety checklist exists.
- Produced artifacts or diagnostic bundles are inspected.
- No secrets, private local files, raw uploaded audio, or development cache files are found in release artifacts.
- Any unavoidable machine/build metadata is documented.
- If artifacts cannot be inspected, the release is blocked from external sharing.

Validation:

- Manual artifact inspection.
- CI artifact review or documented blocker.
- QA review.

Release Impact:

- Required before installer artifacts can be shared outside the core development team.

Implementation Notes:

- Added `docs/sprints/sprint-03-release-artifact-safety-review.md`.
- Reviewed artifacts from GitHub Actions run `27737626166`.
- Downloaded and expanded `harmonIA-windows-diagnostic-logs` and `harmonIA-windows-internal-installers` outside the repository.
- Checked artifact names and contents for `.env`, secret, private local path, raw audio, upload-folder, cache, and temp-folder indicators.
- Administratively extracted the MSI and scanned the extracted app executable.
- Documented expected GitHub runner build paths and Windows manifest `publicKeyToken` false positives.
- Kept external sharing blocked pending RLS3-002, RLS3-003, and explicit user approval.

Validation Result:

- Artifact safety checklist completed.
- Produced installer and diagnostic artifacts were inspected.
- No leaked secrets, private developer-machine files, raw uploaded audio, or development cache files were found.
- Unavoidable build metadata was documented.
- External sharing remains blocked until the remaining release-safety cards pass.

Handoff:

```text
Agent: Linus (Release Coordinator)
Scope: RLS3-001 release artifact safety review.
Changed: Added the Sprint 03 artifact safety report and recorded artifact inspection results.
Validated: Downloaded and expanded CI artifacts; reviewed names, logs, Tauri config snapshot, bundle manifest, MSI extraction output, binary strings, and checksums.
Risks: NSIS installer was not deeply extracted because no dedicated NSIS extraction tool was available; external sharing remains blocked by RLS3-002 and RLS3-003.
Next: Ada can proceed with RLS3-002, and Linus can reuse the recorded checksums for RLS3-003.
```

### RLS3-002: Installer Permissions And Data Boundary Review

GitHub Issue: `#16`
Agent Owner: Ada
Supporting: Pixel, Grace, Linus
Status: Done
Dependency: SS3-001, SS3-004 as applicable

Value:

The installer and desktop app should not request or imply more system access than harmonIA needs for the connected upload workflow.

In Scope:

- Review Tauri permissions and capabilities.
- Review file-picker and drag-and-drop behavior.
- Confirm uploaded local files are selected by the user and only submitted when analysis starts.
- Confirm the desktop app does not read arbitrary directories.
- Document local data boundaries and current storage behavior.
- Document what network endpoints the app can contact through configuration.

Out of Scope:

- Full sandbox hardening.
- Offline model storage.
- Enterprise device management policy.

Acceptance Criteria:

- Permission/data-boundary review document exists.
- Required desktop permissions are listed.
- User-selected-file behavior is documented.
- Network/API target behavior is documented.
- Any risky permission or unclear boundary creates a follow-up card before public distribution.

Validation:

- EM review.
- QA manual flow review.
- Desktop tests remain green.

Release Impact:

- Required before describing the installer as safe for non-developer testers.

Review Result:

- Added `docs/distribution/installer-permissions-data-boundary-review.md`.
- Passed for Sprint 03 internal distribution review.
- Current Tauri shell does not declare native plugins, custom commands, or app-specific capability grants.
- Current desktop code uses browser file input and drag/drop `File` objects; selected files are held in React memory and submitted only when the user starts analysis.
- No arbitrary directory reads, native filesystem API usage, browser persistence API usage, or local audio copy behavior were found in the reviewed desktop app code.
- Network behavior is documented as browser `fetch` to the configured API base URL, defaulting to `http://127.0.0.1:8000`.
- Follow-up risks are documented for production CSP/API target allow-listing, future Tauri plugin capabilities, backend uploaded-audio retention, and clean-machine validation.

QA Review:

- Grace reviewed Ada's RLS3-002 document against `App.tsx`, `App.test.tsx`, `jobs.ts`, `jobs.test.ts`, `Cargo.toml`, `main.rs`, `tauri.conf.json`, and the Tauri capabilities directory state.
- QA confirmed the manual upload-flow boundary: a single user-selected or dropped browser `File` is validated, held in React memory, and uploaded only after `Run analysis`.
- QA confirmed the API client appends the selected file as multipart field `file` and posts it to `/v1/jobs/upload`.
- QA confirmed source search found no browser persistence APIs, object URL creation, `FileReader`, directory upload, privileged Tauri IPC, or Tauri filesystem/dialog/shell usage in the reviewed desktop code.
- `npm run desktop:test` passed with 25 tests across 3 files.
- `apps/desktop/src-tauri/tauri.conf.json` parsed as valid JSON.
- QA did not install the MSI or EXE on the host; SS3-004 remains the clean-machine installer execution gate.

Handoff:

```text
Agent: Ada (Engineering Manager)
Scope: RLS3-002 installer permissions and desktop data boundary review.
Changed: Added the installer permissions and data boundary review document; documented current Tauri permission surface, file-selection flow, local storage behavior, and API target behavior.
Validated: Reviewed desktop source/tests, Tauri config/Rust shell, release artifact safety review, Windows diagnostic workflow, WebView2 strategy, and Tauri permission/capability docs; searched for privileged Tauri APIs and browser persistence APIs; did not install MSI or EXE on the host.
Risks: Production CSP/API target allow-list is not defined; future Tauri plugins need scoped capabilities; backend uploaded-audio retention is outside this review; clean-machine install remains blocked until SS3-004 can run in a clean VM or Windows Sandbox.
Next: Main thread can review and update GitHub issue #16; Linus can proceed with RLS3-003 using this review as a sharing gate input.
```

```text
Agent: Grace (QA)
Scope: RLS3-002 QA validation of Ada's installer permissions and data boundary review.
Changed: Added QA review evidence to the Sprint 03 card and the RLS3-002 distribution review document.
Validated: Reviewed Ada's document, sprint card, desktop upload flow, API upload client, desktop tests, Tauri config/Rust shell, Cargo dependencies, and capability directory state; ran desktop tests and parsed the Tauri config JSON; did not install MSI or EXE on the host.
Risks: Clean-machine installer execution remains unvalidated until SS3-004 can run in Windows Sandbox or a clean VM; production CSP/API allow-listing and backend uploaded-audio retention remain future hardening items before wider distribution.
Next: Main thread can update GitHub issue #16; Linus can use the QA-signed RLS3-002 evidence for RLS3-003 while keeping SS3-004 as the install gate.
```

### RLS3-003: Internal Sharing, Provenance, And Integrity Checklist

GitHub Issue: `#17`
Agent Owner: Linus
Supporting: Grace, Ada
Status: Done
Dependency: SS3-003, RLS3-001

Value:

Internal testers need to know exactly which artifact they are installing, where it came from, and whether it is approved for sharing.

In Scope:

- Define internal-only artifact naming rules.
- Record source commit SHA and tag/release target.
- Generate or document artifact checksums when artifacts exist.
- Document who may receive installer artifacts.
- Document that unsigned artifacts may trigger Windows warnings.
- Define what blocks artifact sharing.

Out of Scope:

- Public release publication.
- Code signing implementation.
- Automatic update infrastructure.

Acceptance Criteria:

- Internal sharing checklist exists.
- Artifact provenance fields are defined.
- Checksum expectations are documented.
- Unsigned-installer warnings are documented.
- External sharing remains blocked unless user approval is explicit.

Validation:

- Release Coordinator review.
- QA confirms checklist is understandable.

Release Impact:

- Required before distributing installers to internal testers outside the development machine.
- External sharing remains blocked because SS3-004 clean-machine installation validation is blocked and the user has not explicitly approved sharing beyond the core development team.

Implementation Notes:

- Added `docs/distribution/internal-artifact-sharing-provenance.md`.
- Recorded the current Sprint 03 provenance fields for GitHub Actions run `27737626166`, source commit `12475db1bf9b07bf832e55c21d8cd4110de6d33d`, installer artifact ID `7714638513`, diagnostic artifact ID `7714638787`, artifact digests, and artifact expiration.
- Documented the release target as `v0.4.0` while preserving the generated installer version/filenames at `0.3.0`.
- Documented MSI, NSIS, and extracted app executable SHA-256 checksums from the RLS3-001 safety review.
- Defined internal container naming rules, manifest expectations, approved recipient boundaries, unsigned-installer warnings, and sharing blockers.
- Confirmed this card does not upload artifacts, share artifacts, install MSI/EXE, create public releases, implement code signing, or bypass SS3-004.

Validation Result:

- Release Coordinator review completed against SS3-003, RLS3-001, RLS3-002, SS3-004, and SS3-006 evidence.
- Checksum expectations and Windows PowerShell verification commands are documented.
- Current approved recipients are limited to the core development/release reviewers; Grace or an approved QA operator may receive artifacts only to perform SS3-004 in a clean VM/Sandbox.
- Non-developer tester sharing, external sharing, public release links, GitHub Releases, app-store distribution, and production claims remain blocked.
- No GitHub issue update was made from this Linus pass.

QA Review:

- Grace reviewed the RLS3-003 checklist for readability and usability.
- QA found the checklist understandable and usable for internal artifact handling because it clearly separates provenance, checksums, recipient boundaries, unsigned-installer warnings, blockers, and pre-share steps.
- QA did not install, execute, upload, move, or share MSI/EXE artifacts.
- No GitHub issue update was made from this Grace pass.

Handoff:

```text
Agent: Linus (Release Coordinator)
Scope: RLS3-003 internal sharing, provenance, and integrity checklist.
Changed: Added the internal artifact sharing/provenance policy, recorded current Sprint 03 artifact provenance, documented checksum expectations, recipient boundaries, unsigned-installer warnings, and sharing blockers.
Validated: Reused SS3-003 run evidence, RLS3-001 artifact IDs/digests/checksums, RLS3-002 permission/data-boundary result, SS3-004 blocked QA result, and SS3-006 signing decision; did not upload/share artifacts, install MSI/EXE, or create public releases.
Risks: SS3-004 clean-machine installation remains blocked; artifacts are unsigned; GitHub-hosted artifacts expire on 2026-06-25; non-developer and external sharing remain blocked without explicit user approval.
Next: Main thread can review and update GitHub issue #17; Grace can use this checklist when a clean VM/Sandbox is available for SS3-004.
```

```text
Agent: Grace (QA)
Scope: RLS3-003 QA readability and usability review for the internal sharing/provenance checklist.
Changed: Added QA review evidence to the RLS3-003 provenance document and Sprint 03 card.
Validated: Reviewed the provenance record, checksum instructions, naming rules, recipient boundaries, unsigned-installer warning, sharing blockers, and pre-share checklist; did not install, execute, upload, move, or share MSI/EXE artifacts.
Risks: SS3-004 clean-machine installation remains blocked; external sharing still requires passing SS3-004 and explicit user approval for the named sharing scope.
Next: Main thread can update GitHub issue #17; Grace can reuse this checklist when a clean VM/Sandbox is available for SS3-004.
```

### SS3-007: QA Review and Distribution Regression Coverage

GitHub Issue: `#18`
Agent Owner: Grace
Supporting: Turing, Pixel, Ada, Linus
Status: Done
Dependency: SS3-001, SS3-002, SS3-003, SS3-004, RLS3-001, RLS3-002, RLS3-003 as applicable

Value:

Sprint 03 needs a clear quality record because distribution failures can be environment-specific and hard to reproduce.

In Scope:

- Review implementation tests and workflow logs.
- Add regression coverage for changed desktop configuration behavior.
- Document manual smoke checks.
- Document clean-machine testing results or blocker.
- Review release-safety cards and artifact sharing status.
- Confirm existing upload flow remains stable.

Out of Scope:

- Full automated desktop E2E framework.
- Production monitoring.
- Signed release validation.

Acceptance Criteria:

- QA report is added for Sprint 03.
- Automated and manual coverage are documented.
- Known gaps are explicit.
- Release-safety findings are recorded.
- Validation command results are recorded.

Validation:

- `npm audit`
- `npm run desktop:test`
- `npm run desktop:build`
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests`
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai`
- CI workflow result or documented blocker.

Release Impact:

- Required before `v0.4.0` release recommendation.

Implementation Notes:

- Added `docs/sprints/sprint-03-qa-report.md`.
- Added desktop regression coverage for oversized audio-file validation.
- Remediated the high-severity npm audit finding by updating the lockfile from `undici@7.26.0` to `undici@7.28.0`.
- Recorded that SS3-004 clean-machine validation remains blocked because Windows Sandbox or a clean VM is not available from this workspace.
- Confirmed that release-safety evidence supports release preparation, but not external installer sharing.

Validation Result:

- `npm audit --audit-level=high` initially failed because `jsdom` resolved `undici@7.26.0`; `npm audit fix` updated the lockfile to `undici@7.28.0`.
- `npm audit --audit-level=high` passed after the lockfile update with `found 0 vulnerabilities`.
- `npm run desktop:test` passed with 26 tests across 3 files.
- `npm run desktop:build` passed.
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` passed with 18 tests.
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai` passed.
- GitHub Actions Windows diagnostic workflow run `27737626166` passed earlier in Sprint 03.

Handoff:

```text
Agent: Grace (QA)
Scope: SS3-007 QA review and distribution regression coverage.
Changed: Added oversized-audio regression coverage, remediated the npm audit lockfile finding, and documented Sprint 03 QA evidence.
Validated: npm audit; npm run desktop:test; npm run desktop:build; backend/worker pytest; Python compileall; reviewed Windows CI run 27737626166 and release-safety documents.
Risks: Clean-machine installer execution remains blocked; installer artifacts are unsigned; external sharing remains blocked until SS3-004 passes and the user explicitly approves the sharing scope.
Next: Linus can prepare SS3-008 release notes and request user approval before creating the v0.4.0 tag.
```

### SS3-008: Release v0.4.0

GitHub Issue: `#19`
Agent Owner: Linus
Supporting: Atlas, Grace, Ada, Maestro
Status: Done
Dependency: SS3-001 through SS3-007 and RLS3-001 through RLS3-003

Value:

The team needs a tested release checkpoint after connected desktop distribution readiness work.

In Scope:

- Confirm product scope with Maestro.
- Confirm technical readiness with Ada.
- Run or review full validation suite.
- Prepare release notes.
- Confirm release-safety gates and artifact sharing status.
- Document known limitations and rollback suggestion criteria.
- Tag `v0.4.0` only after validation passes and user approval is given.

Out of Scope:

- Automatic rollback.
- Publishing unsigned installers as production-ready.
- Sharing installer artifacts externally before safety gates pass.
- Purchasing signing certificates.

Acceptance Criteria:

- Release notes are prepared.
- Validation results are recorded.
- Installer artifact status is explicit.
- Release-safety status is explicit.
- External sharing remains blocked unless explicitly approved.
- Rollback suggestion criteria are documented.
- User approval is received before tagging.

Validation:

- `npm audit`
- `npm run desktop:build`
- `npm run desktop:test`
- `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests`
- `.venv\Scripts\python.exe -m compileall apps\api workers\ai`
- GitHub Actions Windows workflow result or documented blocker.
- Clean-machine validation result or documented blocker.
- Release artifact safety review result or documented blocker.

Release Impact:

- Creates the `v0.4.0` release checkpoint.

Release Review:

- Release notes prepared in `docs/releases/v0.4.0.md`.
- QA report completed in `docs/sprints/sprint-03-qa-report.md`.
- Validation gates passed for audit, desktop tests, desktop build, backend/worker tests, and Python compile.
- Windows diagnostic workflow run `27737626166` passed earlier in Sprint 03 and produced internal diagnostic artifacts.
- RLS3-001, RLS3-002, and RLS3-003 are complete.
- SS3-004 remains blocked because clean-machine installation requires Windows Sandbox or a clean VM that is not available from this workspace.
- External installer sharing remains blocked.
- User approved proceeding with SS3-008 on 2026-06-19.
- Version metadata was bumped to `0.4.0`.
- Release gates passed after the version metadata bump.
- The `v0.4.0` tag is approved for creation from the release metadata commit.

Handoff:

```text
Agent: Linus (Release Coordinator)
Scope: SS3-008 v0.4.0 release preparation.
Changed: Prepared v0.4.0 release notes, recorded release readiness, known limitations, installer sharing status, and rollback suggestion criteria.
Validated: Reused SS3-007 validation results, Windows diagnostic workflow run 27737626166, and RLS3-001 through RLS3-003 release-safety evidence; reran release gates after the metadata bump.
Risks: SS3-004 clean-machine installation is blocked; installer artifacts are unsigned/internal-only; external sharing remains blocked.
Next: Push the v0.4.0 tag and run post-release validation.
```

## Recommended Sequencing

1. SS3-001 and SS3-002 can start first after approval.
2. SS3-005 should be decided before treating installer artifacts as release-ready.
3. SS3-003 can start after SS3-005 or proceed as diagnostic CI if WebView2 is still under review.
4. RLS3-001 starts after CI produces artifacts or diagnostic bundles.
5. SS3-004 depends on installer artifacts or a documented CI blocker.
6. RLS3-002 can start after SS3-001 and clean-machine observations where available.
7. RLS3-003 starts after artifact safety review.
8. SS3-006 can run in parallel because it is planning-only.
9. SS3-007 and SS3-008 close the sprint.

## Sprint Risks

- Native Tauri builds timed out locally during the `v0.3.0` release attempt.
- GitHub Actions may expose missing Rust, system, or WebView2 packaging dependencies.
- No hosted staging or production API exists yet.
- Clean-machine testing needs access to Windows Sandbox or a clean VM.
- Code signing may require paid certificates and identity verification.
- Installer strategy decisions can affect file size and first-run user experience.
- Installer artifacts could accidentally include local files, logs, or internal configuration unless release-safety checks are treated as gates.
- Shipping installer polish too early could cause rework; Sprint 03 should prioritize diagnostics and safety before final packaging.

## Definition Of Ready For Sprint Start

- User approves this sprint plan.
- Maestro confirms product scope.
- Ada confirms architecture constraints.
- Atlas confirms GitHub issue statuses and ownership.
- SS3-007, SS3-008, and RLS3-001 through RLS3-003 GitHub issues are created if approved.
- Existing SS3 issue bodies are updated from draft text if approved.

## Definition Of Done

- Approved cards are Done or explicitly Deferred.
- Validation gates pass or blockers are documented.
- QA report is complete.
- Release notes are prepared.
- RLS safety gates are complete or documented as blockers.
- User approved the `v0.4.0` release checkpoint on 2026-06-19.
- Distribution limitations are clear and visible.
- Installer artifacts are not shared externally unless explicitly approved.
