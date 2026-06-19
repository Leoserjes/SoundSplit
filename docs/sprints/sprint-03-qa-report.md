# Sprint 03 QA Report

Status: Complete for SS3-007
GitHub Issue: `#18`
Owner: Grace - QA
Execution note: Completed from the main coordination thread after the Grace worker was interrupted by account usage limits.
Review Date: 2026-06-19

## QA Decision

Sprint 03 has enough automated and documentation evidence to proceed to release preparation for `v0.4.0`.

QA does not approve external installer sharing yet. SS3-004 clean-machine installation remains blocked because this workspace does not provide Windows Sandbox or a clean VM, and MSI/EXE artifacts were not installed on the host machine.

## Evidence Reviewed

- SS3-001 environment-aware desktop API configuration.
- SS3-002 single-command local developer startup.
- SS3-003 Windows diagnostic build workflow and successful run `27737626166`.
- SS3-004 clean-machine installation blocker report.
- SS3-005 WebView2 strategy decision.
- SS3-006 Windows code-signing plan.
- RLS3-001 release artifact safety review.
- RLS3-002 installer permissions and data-boundary review.
- RLS3-003 internal sharing, provenance, and integrity checklist.
- Desktop upload-flow tests and API client tests.

## Automated Validation

Validation was run from the repository root on 2026-06-19.

| Command | Result |
| --- | --- |
| `npm audit --audit-level=high` | Initially failed because `jsdom` resolved `undici@7.26.0` with high-severity advisories. |
| `npm audit fix` | Updated the lockfile to `undici@7.28.0`. |
| `npm audit --audit-level=high` | Passed after the lockfile update; npm reported `found 0 vulnerabilities`. |
| `npm run desktop:test` | Passed with 26 tests across 3 files. |
| `npm run desktop:build` | Passed; Vite completed the production build. |
| `.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests` | Passed with 18 tests. |
| `.venv\Scripts\python.exe -m compileall apps\api workers\ai` | Passed. |

GitHub Actions Windows diagnostic workflow run `27737626166` passed earlier in Sprint 03 and produced internal installer plus diagnostic-log artifacts.

## Regression Coverage Added

Added desktop test coverage for oversized audio-file validation in `apps/desktop/src/App.test.tsx`.

The new test verifies that a file larger than 100 MB is rejected with the expected validation message and is not kept as the selected upload candidate. This extends the existing upload-flow regression coverage for unsupported file types, empty files, upload failures, dropped files, and duplicate submission prevention.

## Manual And Release-Safety Findings

RLS3-001 passed for the reviewed CI artifacts. No leaked secrets, private developer-machine files, raw uploaded audio, or development cache files were found in the inspected artifacts. NSIS deep extraction remains a noted limitation because a dedicated NSIS extraction tool was not available.

RLS3-002 passed for Sprint 03 internal distribution review. The current desktop app uses browser-selected `File` objects, does not expose privileged Tauri filesystem/dialog/shell/process APIs, does not read arbitrary directories, and submits the selected file only after `Run analysis`.

RLS3-003 completed the provenance, checksum, recipient, unsigned-installer warning, and sharing-blocker checklist. Current installer artifacts remain internal release evidence only.

SS3-004 remains blocked. No clean-machine install, launch, API-unavailable smoke, WebView2 prompt, SmartScreen prompt, or uninstall result can be claimed until Windows Sandbox or a clean VM is available.

SS3-006 keeps Windows code signing deferred for `v0.4.0`. Installer artifacts remain unsigned internal diagnostics.

## Release Guidance

QA supports moving to SS3-008 release preparation with these constraints:

- The `v0.4.0` release notes must state that installer artifacts are unsigned internal diagnostics.
- The release notes must state that clean-machine installation is blocked and not yet validated.
- External sharing remains blocked unless SS3-004 later passes and the user explicitly approves the named sharing scope.
- The release tag must not be created until the user approves SS3-008.

## Handoff

```text
Agent: Grace (QA)
Scope: SS3-007 QA review and distribution regression coverage.
Changed: Added oversized-audio regression coverage, remediated the npm audit lockfile finding, and documented Sprint 03 QA evidence.
Validated: npm audit; npm run desktop:test; npm run desktop:build; backend/worker pytest; Python compileall; reviewed Windows CI run 27737626166 and release-safety documents.
Risks: Clean-machine installer execution remains blocked; installer artifacts are unsigned; external sharing remains blocked until SS3-004 passes and the user explicitly approves the sharing scope.
Next: Linus can prepare SS3-008 release notes and request user approval before creating the v0.4.0 tag.
```
