# SS3-004 Clean-Machine Installation QA

Status: Deferred - clean Windows Sandbox or clean VM not available in this workspace
GitHub Issue: `#4`
Owner: Grace - QA
Supporting: Linus, Pixel, Ada
Review Date: 2026-06-19

## QA Decision

SS3-004 is deferred out of Sprint 03.

The Sprint 03 release checkpoint is complete, but a valid clean-machine installation test still requires Windows Sandbox or a clean VM. This workspace does not currently provide a usable clean environment, and the MSI/EXE must not be installed on the host machine.

Grace keeps the validation requirements intact and marks this card deferred until a clean Windows Sandbox or clean VM is available. The card should not be interpreted as a passed installer validation.

## Artifact Source To Use

Use the fresh `v0.4.0` internal diagnostic artifacts from the post-release Windows workflow when the clean-machine environment becomes available. These artifacts have not been approved for external sharing; RLS artifact safety/provenance evidence must be refreshed before any sharing decision.

| Field | Value |
| --- | --- |
| Workflow run | `27800606772` |
| Run URL | `https://github.com/Leoserjes/SoundSplit/actions/runs/27800606772` |
| Reviewed commit | `7b5656df6494a90511086405648962caa349e9f0` |
| Installer artifact | `harmonIA-windows-internal-installers` |
| Installer artifact ID | `7740186092` |
| Installer artifact digest | `sha256:1da69737665417b1b313a2d6122cd70ef2ac2a4ebfa9a0d7da20e7dd79735fec` |
| Artifact expiration | 2026-06-26 |
| MSI | `msi/harmonIA_0.4.0_x64_en-US.msi` |
| MSI SHA-256 | `d81ba8fd2db6e139a9a66d4e6aeb9bf58e6e3e9b2faf57cd093a314b352b1780` |
| NSIS | `nsis/harmonIA_0.4.0_x64-setup.exe` |
| NSIS SHA-256 | `c2b7099c9ae05973c4942c1426735fc119f3579199fa98990b50d9a155a5adf8` |

Do not use locally rebuilt installers for this card unless the source run, commit, artifact name, and checksums are recorded again.

## Current Environment Check

The host machine was checked only for clean-environment availability:

| Check | Result |
| --- | --- |
| Host MSI/EXE installation | Not performed |
| Current session elevated/admin | No |
| `C:\WINDOWS\System32\WindowsSandbox.exe` | Not found |
| `Containers-DisposableClientVM` optional feature query | Unavailable from current non-elevated session; Windows reported that elevation is required |
| `Microsoft-Hyper-V-All` optional feature query | Unavailable from current non-elevated session; Windows reported that elevation is required |
| Hyper-V Manager path | Not found |
| Clean VM available to this workspace | Not found |

Because no clean Windows Sandbox or clean VM is available, no install, launch, API, permission, or uninstall result can be claimed for SS3-004 yet.

## QA Recommendation

- Close SS3-004 as Deferred for Sprint 03 so the released sprint is not left with a permanently open environment blocker.
- Reopen this validation or create a follow-up clean-machine card when Windows Sandbox or a clean VM is available.
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

- [ ] Install `msi/harmonIA_0.4.0_x64_en-US.msi`.
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
- [ ] Install `nsis/harmonIA_0.4.0_x64-setup.exe`.
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

Future clean-machine validation can move forward only when:

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
Changed: Deferred SS3-004 from Sprint 03 with a preserved clean-machine checklist, refreshed v0.4.0 artifact source, current environment precheck, and explicit sharing limits.
Validated: Checked current clean-environment availability; confirmed this session is not elevated, Windows Sandbox is not installed, optional feature queries require elevation, Hyper-V Manager is not present, and no clean VM is available; downloaded the fresh v0.4.0 internal installer artifact only to compute MSI/NSIS SHA-256 hashes; did not install MSI or EXE on the host machine.
Risks: No actual clean-machine install has been performed; current installer artifacts are still not approved for non-developer testers or external sharing; connected API success may require a future staging API build or explicit clean-machine backend setup.
Next: Provide a Windows Sandbox or clean VM, rerun this checklist against the recorded artifacts, then create or reopen a clean-machine validation card with observed pass/fail evidence.
```
