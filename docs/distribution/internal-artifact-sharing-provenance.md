# Internal Artifact Sharing, Provenance, And Integrity Checklist

Status: Done for Sprint 03 checklist/provenance policy
External sharing: Blocked
Owner: Linus - Release Coordinator
Supporting evidence: RLS3-001, RLS3-002, SS3-003, SS3-004, SS3-006
Review Date: 2026-06-18

## Purpose

This checklist defines how Sprint 03 Windows installer artifacts may be identified, verified, and discussed before any internal or external sharing.

It does not approve public release publication, artifact upload to a new location, installer execution on the host machine, code signing, or distribution to non-approved testers.

## Current Sharing Decision

The Sprint 03 installer artifacts remain internal release evidence only.

Do not share the MSI or NSIS installer with non-developer testers yet. External sharing is blocked because SS3-004 clean-machine installation validation is blocked, the artifacts are unsigned, and the user has not explicitly approved sharing beyond the core development team.

## Provenance Record

| Field | Current Sprint 03 Value |
| --- | --- |
| Release target | `v0.4.0` connected desktop distribution checkpoint |
| Product/app version in generated installers | `0.3.0` |
| Workflow run | `27737626166` |
| Workflow run URL | `https://github.com/Leoserjes/SoundSplit/actions/runs/27737626166` |
| Source commit SHA | `12475db1bf9b07bf832e55c21d8cd4110de6d33d` |
| Source commit summary | `ci: avoid Windows builds for sprint doc updates` |
| Installer artifact name | `harmonIA-windows-internal-installers` |
| Installer artifact ID | `7714638513` |
| Installer artifact digest | `sha256:1fb662dc68f80e181f75a942dd890408bacad4a8d1d07fa52a04120906effc73` |
| Diagnostic artifact name | `harmonIA-windows-diagnostic-logs` |
| Diagnostic artifact ID | `7714638787` |
| Diagnostic artifact digest | `sha256:1419a5fda19ca344e9f0191e79040249c912be50b1cc8b930a4dc3e2d0376609` |
| Artifact expiration | 2026-06-25 |
| Safety review | `docs/sprints/sprint-03-release-artifact-safety-review.md` |
| Permission/data-boundary review | `docs/distribution/installer-permissions-data-boundary-review.md` |
| Clean-machine install status | Blocked; no clean VM or Windows Sandbox validation has run |
| Signing status | Deferred; installers are unsigned internal diagnostics |

The `v0.4.0` release target and `0.3.0` generated installer filenames are intentionally recorded separately. Do not manually rename the installer files to hide this mismatch. If a future sharing bundle is created, put target/version/run information in the containing folder, manifest, or release notes, not by editing the produced installer binaries.

## Artifact Checksums

Canonical checksum evidence lives in `docs/sprints/sprint-03-release-artifact-safety-review.md`.

| File | Size | SHA-256 |
| --- | ---: | --- |
| `msi/harmonIA_0.3.0_x64_en-US.msi` | 2,764,800 | `3f8d31dc6d02807623d2a6aae8a9c51becc6e14ec41049a8e110e4b30e77ca2d` |
| `nsis/harmonIA_0.3.0_x64-setup.exe` | 1,831,707 | `f9f05f8bc27de25ee3de79352453688ffedb3bcab3326fea62e1c78a0fa39d2e` |
| `PFiles/harmonIA/harmonia.exe` | 8,233,984 | `875c50b89b0d8873646961ee5279bc1ef2977fcd92b2d597ccb47b628f095dcf` |

Before any approved recipient installs an artifact in a clean environment, the recipient or release coordinator must verify the SHA-256 hash of the installer file. On Windows:

```powershell
Get-FileHash -Algorithm SHA256 .\harmonIA_0.3.0_x64_en-US.msi
Get-FileHash -Algorithm SHA256 .\harmonIA_0.3.0_x64-setup.exe
```

Any checksum mismatch blocks installation and sharing.

## Internal Naming Rules

- Keep the original installer filenames produced by CI.
- When a transfer folder, zip, or manifest is created later, name that container with the release target, workflow run, source short SHA, and sharing date.
- Recommended container name format: `harmonia-v0.4.0-internal-run27737626166-12475db1-YYYYMMDD`.
- Include a manifest beside the installers whenever artifacts are shared.
- The manifest must include the provenance fields, per-file SHA-256 checksums, unsigned-installer warning, recipient name or group, sharing date, and approval reference.
- Never put secrets, `.env` values, raw uploaded audio, private machine paths, or local inspection logs into the sharing container.

## Approved Recipients

Current approved recipients:

- Core development/release reviewers only: Ada, Maestro, Turing, Pixel, Grace, Linus, Atlas, and the user.
- Grace or an approved QA operator may receive the artifacts only to run SS3-004 inside Windows Sandbox or a clean VM.

Not approved yet:

- Non-developer testers.
- External collaborators.
- Public download links.
- GitHub Releases, website downloads, app stores, package managers, or social sharing.

Before any non-developer tester receives an installer, SS3-004 must pass, RLS3-003 evidence must still match the artifact being shared, and the user must explicitly approve the named sharing scope.

## Unsigned Installer Warning

The Sprint 03 MSI and NSIS artifacts are unsigned internal diagnostics. Windows SmartScreen, Microsoft Defender, browser download protection, or enterprise device policy may warn, quarantine, or block the installers.

Recipients must be told before receiving the artifacts:

- The installer is unsigned.
- The artifact is not a public production release.
- Warnings are expected and should be documented, not silently dismissed.
- Enterprise or managed-device security policy must not be bypassed.
- Any warning, quarantine, or installation block should be reported with the artifact name, checksum, machine type, Windows version, and screenshot or exact message where practical.

Code signing remains deferred by `docs/distribution/windows-code-signing-plan.md`.

## Sharing Blockers

Do not share, install, or promote an installer artifact if any blocker below is true:

- Source run, commit SHA, artifact ID, artifact digest, or file checksum is missing.
- Downloaded artifact digest or installer checksum does not match the recorded value.
- Artifact comes from a local rebuild or different CI run without a fresh provenance record.
- RLS3-001 safety review is missing, failed, or stale for the artifact being shared.
- RLS3-002 permission/data-boundary review is missing, failed, or stale for the artifact being shared.
- SS3-004 clean-machine installation validation is blocked or failed, except when the artifact is being sent only to Grace or an approved QA operator to perform that validation in a clean VM/Sandbox.
- The recipient is not explicitly approved for the current sharing scope.
- The user has not explicitly approved sharing beyond the core development team.
- The artifact is being positioned as public, production-ready, signed, offline-capable, or safe for broad distribution.
- The sharing container would include secrets, `.env` files, raw uploaded audio, local inspection logs, development caches, or unrelated workspace files.
- The GitHub artifact has expired and no approved copy with matching checksum and provenance exists.

## Pre-Share Checklist

- [ ] Confirm the sharing purpose and recipient are approved.
- [ ] Confirm the artifact source is GitHub Actions run `27737626166` or record a fresh run.
- [ ] Confirm the full source commit SHA.
- [ ] Confirm artifact ID and digest.
- [ ] Verify installer SHA-256 checksum.
- [ ] Attach or include the provenance manifest.
- [ ] Include unsigned-installer warning language.
- [ ] Confirm RLS3-001 and RLS3-002 still apply.
- [ ] Confirm SS3-004 has passed, unless the recipient is Grace or an approved QA operator performing SS3-004.
- [ ] Confirm user approval exists for any sharing beyond the core development team.
- [ ] Record who received the artifact, when, and for what purpose.

## Result

RLS3-003 is complete for checklist and provenance policy. No artifacts were uploaded, shared, installed, publicly released, or newly published as part of this work.

External sharing remains blocked until SS3-004 passes and the user explicitly approves the named sharing scope.

## Handoff

```text
Agent: Linus (Release Coordinator)
Scope: RLS3-003 internal sharing, provenance, and integrity checklist.
Changed: Added the internal artifact sharing/provenance policy, recorded current Sprint 03 artifact provenance, documented checksum expectations, recipient boundaries, unsigned-installer warnings, and sharing blockers.
Validated: Reused SS3-003 run evidence, RLS3-001 artifact IDs/digests/checksums, RLS3-002 permission/data-boundary result, SS3-004 blocked QA result, and SS3-006 signing decision; did not upload/share artifacts, install MSI/EXE, or create public releases.
Risks: SS3-004 clean-machine installation remains blocked; artifacts are unsigned; GitHub-hosted artifacts expire on 2026-06-25; non-developer and external sharing remain blocked without explicit user approval.
Next: Main thread can review and update GitHub issue #17; Grace can use this checklist when a clean VM/Sandbox is available for SS3-004.
```
