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
Status: Ready
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

### SS3-004: Validate Clean-Machine Installation

GitHub Issue: `#4`
Agent Owner: Grace
Supporting: Linus, Pixel, Ada
Status: Ready
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

### SS3-006: Plan Windows Code Signing

GitHub Issue: `#6`
Agent Owner: Linus
Supporting: Ada, Maestro
Status: Ready
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

- Documentation review by Linus, Ada, and Maestro.

Release Impact:

- Planning artifact only for `v0.4.0`; implementation can be deferred.

### RLS3-001: Release Artifact Safety Review

GitHub Issue: TBD after approval
Agent Owner: Linus
Supporting: Ada, Grace
Status: Ready
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

### RLS3-002: Installer Permissions And Data Boundary Review

GitHub Issue: TBD after approval
Agent Owner: Ada
Supporting: Pixel, Grace, Linus
Status: Ready
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

### RLS3-003: Internal Sharing, Provenance, And Integrity Checklist

GitHub Issue: TBD after approval
Agent Owner: Linus
Supporting: Grace, Ada
Status: Ready
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

### SS3-007: QA Review and Distribution Regression Coverage

GitHub Issue: TBD after approval
Agent Owner: Grace
Supporting: Turing, Pixel, Ada, Linus
Status: Ready
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

### SS3-008: Release v0.4.0

GitHub Issue: TBD after approval
Agent Owner: Linus
Supporting: Atlas, Grace, Ada, Maestro
Status: Ready
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
- User approves any release tag.
- Distribution limitations are clear and visible.
- Installer artifacts are not shared externally unless explicitly approved.
