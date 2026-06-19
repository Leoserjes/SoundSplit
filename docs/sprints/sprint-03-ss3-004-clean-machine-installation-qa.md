# SS3-004 Clean-Machine Installation QA

Status: Blocked - clean Windows Sandbox or clean VM not available in this workspace
GitHub Issue: `#4`
Owner: Grace - QA
Supporting: Linus, Pixel, Ada
Review Date: 2026-06-19

## QA Decision

SS3-004 is not ready for release review or Done.

The Sprint 03 installer artifacts are available for internal validation, and RLS3-001 found no evidence of leaked secrets, private local files, raw uploaded audio, or development cache files in the reviewed artifacts. However, a valid clean-machine installation test requires Windows Sandbox or a clean VM. This workspace does not currently provide a usable clean environment, and the MSI/EXE must not be installed on the host machine.

Grace marks this card blocked until a clean Windows Sandbox or clean VM is available.

## Artifact Source To Use

Use the artifacts already reviewed by RLS3-001:

| Field | Value |
| --- | --- |
| Workflow run | `27737626166` |
| Run URL | `https://github.com/Leoserjes/SoundSplit/actions/runs/27737626166` |
| Reviewed commit | `12475db1bf9b07bf832e55c21d8cd4110de6d33d` |
| Installer artifact | `harmonIA-windows-internal-installers` |
| MSI | `msi/harmonIA_0.3.0_x64_en-US.msi` |
| MSI SHA-256 | `3f8d31dc6d02807623d2a6aae8a9c51becc6e14ec41049a8e110e4b30e77ca2d` |
| NSIS | `nsis/harmonIA_0.3.0_x64-setup.exe` |
| NSIS SHA-256 | `f9f05f8bc27de25ee3de79352453688ffedb3bcab3326fea62e1c78a0fa39d2e` |

Do not use locally rebuilt installers for this card unless the source run, commit, artifact name, and checksums are recorded again.

## Current Environment Check

The host machine was checked only for clean-environment availability:

| Check | Result |
| --- | --- |
| Host MSI/EXE installation | Not performed |
| `C:\WINDOWS\System32\WindowsSandbox.exe` | Not found |
| `Containers-DisposableClientVM` optional feature query | Unavailable from current non-elevated session; Windows reported that elevation is required |
| Clean VM available to this workspace | Not found |

Because no clean Windows Sandbox or clean VM is available, no install, launch, API, permission, or uninstall result can be claimed for SS3-004 yet.

## QA Recommendation

- Keep SS3-004 in Blocked until Grace can run the installer in Windows Sandbox or a clean VM.
- Do not recommend the current installer artifacts for non-developer testers until this checklist passes.
- Test both MSI and NSIS artifacts separately; a pass for one installer format does not automatically pass the other.
- Record unsigned-installer, SmartScreen, UAC, and WebView2 prompts exactly as observed.
- Treat API behavior as two separate checks:
  - default clean-machine behavior with no local API running;
  - connected behavior only when an approved reachable API endpoint or clean-machine backend setup exists.
- Because the current diagnostic build targets the local API URL, clean-machine launch can be tested now, but true connected API success may need a future staging API build or an explicit clean-machine backend setup.

## Repeatable Clean-Machine Checklist

Run this checklist only inside Windows Sandbox or a clean VM snapshot. Do not run it on the developer host.

### 1. Prepare The Machine

- [ ] Record Windows edition, version, build number, and architecture.
- [ ] Record whether the machine has internet access during install.
- [ ] Record whether Microsoft Edge WebView2 Runtime is already installed.
- [ ] Confirm development dependencies are absent or not required:
  - [ ] `where.exe node`
  - [ ] `where.exe npm`
  - [ ] `where.exe python`
  - [ ] `where.exe py`
  - [ ] `where.exe rustc`
  - [ ] `where.exe cargo`
- [ ] Copy only the approved installer artifacts into the clean machine.
- [ ] Verify MSI and NSIS SHA-256 checksums before installation.

### 2. MSI Install Check

- [ ] Install `msi/harmonIA_0.3.0_x64_en-US.msi`.
- [ ] Record any unsigned publisher, SmartScreen, UAC, or WebView2 prompt.
- [ ] Confirm installation completes without requiring Node, npm, Python, Rust, or source checkout files.
- [ ] Launch harmonIA from the installed app entry point.
- [ ] Confirm the desktop window opens without a dev server.
- [ ] Confirm no source path, local developer username, `.env` file, uploaded audio fixture, or cache path appears in the UI.
- [ ] With no local API running, confirm the API unavailable state is understandable and does not crash the app.
- [ ] If an approved reachable API endpoint exists, confirm the configured connected behavior separately.
- [ ] Capture screenshots or exact observation notes for install, launch, and API behavior.
- [ ] Uninstall the MSI build and record whether uninstall succeeds cleanly.

### 3. NSIS Install Check

- [ ] Restore a clean snapshot or start a fresh Windows Sandbox session.
- [ ] Install `nsis/harmonIA_0.3.0_x64-setup.exe`.
- [ ] Record any unsigned publisher, SmartScreen, UAC, or WebView2 prompt.
- [ ] Confirm installation completes without requiring Node, npm, Python, Rust, or source checkout files.
- [ ] Launch harmonIA from the installed app entry point.
- [ ] Confirm the desktop window opens without a dev server.
- [ ] Confirm no source path, local developer username, `.env` file, uploaded audio fixture, or cache path appears in the UI.
- [ ] With no local API running, confirm the API unavailable state is understandable and does not crash the app.
- [ ] If an approved reachable API endpoint exists, confirm the configured connected behavior separately.
- [ ] Capture screenshots or exact observation notes for install, launch, and API behavior.
- [ ] Uninstall the NSIS build and record whether uninstall succeeds cleanly.

## Evidence Template

Use this table when the clean-machine run is available:

| Field | MSI Result | NSIS Result |
| --- | --- | --- |
| Clean environment type |  |  |
| Windows version/build |  |  |
| Internet available during install |  |  |
| WebView2 present before install |  |  |
| Installer checksum matched |  |  |
| Install completed |  |  |
| Unsigned/SmartScreen/UAC prompt observed |  |  |
| WebView2 prompt observed |  |  |
| App launched without dev dependencies |  |  |
| API unavailable behavior documented |  |  |
| Connected API behavior documented |  |  |
| Data-leak/source-path observation |  |  |
| Uninstall completed |  |  |
| Screenshots or notes captured |  |  |

## Pass Criteria

SS3-004 can move forward only when:

- A Windows Sandbox or clean VM run is completed.
- Installer source, workflow run, commit, artifact name, and checksums are recorded.
- At least one installer format launches without Node, npm, Python, Rust, or a source checkout.
- API unavailable behavior is documented.
- Connected API behavior is either validated or explicitly deferred with the reason.
- Data-leak and permission observations are documented.
- Grace leaves a follow-up QA handoff with exact results.

## Handoff

```text
Agent: Grace (QA)
Scope: SS3-004 clean-machine installation validation.
Changed: Added the SS3-004 QA recommendation, blocker rationale, artifact source, clean-environment precheck, repeatable MSI/NSIS checklist, evidence template, and pass criteria.
Validated: Reviewed the Sprint 03 SS3-004 card, RLS3-001 artifact safety report, WebView2 strategy, and Grace QA instructions; checked that Windows Sandbox is not available from this workspace; did not install MSI or EXE on the host machine.
Risks: No actual clean-machine install has been performed; current installer artifacts are still not approved for non-developer testers; connected API success may require a future staging API build or explicit clean-machine backend setup.
Next: Provide a Windows Sandbox or clean VM, rerun this checklist against the recorded artifacts, then update SS3-004 with observed pass/fail evidence.
```
