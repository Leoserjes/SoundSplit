# Windows Diagnostic Build Workflow

Status: Sprint 03 internal diagnostic workflow
Owner: Linus - Release Coordinator
Supporting: Ada - Engineering Manager, Pixel - Front-End Developer, Grace - QA
Last reviewed: 2026-06-18

## Purpose

`.github/workflows/windows-diagnostic-build.yml` provides the first clean Windows CI signal for harmonIA distribution readiness. It is not a publishing workflow and must not be treated as approval to share installer artifacts externally.

## Triggering

The workflow can be triggered manually from GitHub Actions through `workflow_dispatch`.

It also runs on pushes to `master` that touch distribution-relevant files:

- the workflow file
- API, desktop, worker, and contract source files
- package manifests and lockfile
- Sprint 03 and distribution docs

## Validation Gates

The workflow runs these gates before native packaging:

```powershell
npm audit --audit-level=high
npm run dev:check
npm run desktop:test
npm run desktop:build
python -m pytest --rootdir=. apps\api\tests workers\ai\tests
python -m compileall apps\api workers\ai
Get-Content apps\desktop\src-tauri\tauri.conf.json | ConvertFrom-Json | Out-Null
```

The native Tauri build runs only after those gates pass.

## Artifact Policy

Uploaded installer artifacts are internal diagnostics only:

- `harmonIA-windows-internal-installers`
- retention: 7 days
- contents: only MSI/EXE files from `apps/desktop/src-tauri/target/release/bundle`

Diagnostic logs are uploaded regardless of success or failure:

- `harmonIA-windows-diagnostic-logs`
- retention: 7 days
- contents: build log, tool versions, Tauri config snapshot, and bundle file manifest

The workflow intentionally does not upload broad workspace folders. It must not upload `.env` files, local audio files, raw uploads, caches, or unrelated build directories.

## Secrets And Permissions

No repository secrets are required for this diagnostic workflow.

The workflow uses read-only repository contents permission:

```yaml
permissions:
  contents: read
```

Code signing, release creation, and public publishing are out of scope.

## Expected Follow-Ups

- RLS3-001 must inspect produced artifacts before any external sharing.
- RLS3-003 must record artifact provenance and sharing rules.
- SS3-004 should use workflow artifacts, if available, for clean-machine validation.
- SS3-006 should define the future signing path before public installer distribution.
