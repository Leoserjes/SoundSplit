# Sprint 03 Release Artifact Safety Review

Status: Passed for internal-only review
GitHub Issue: `#15`
Owner: Linus
Supporting: Ada, Grace
Reviewed Run: `27737626166`
Run URL: https://github.com/Leoserjes/SoundSplit/actions/runs/27737626166
Reviewed Commit: `12475db1bf9b07bf832e55c21d8cd4110de6d33d`
Review Date: 2026-06-18

## Scope

This review checks the Sprint 03 Windows diagnostic artifacts for accidental inclusion of secrets, private local files, raw uploaded audio, development caches, or unsafe diagnostic content.

This review does not approve public distribution. Installer sharing remains internal-only until RLS3-002 and RLS3-003 are complete and the user explicitly approves sharing.

## Reviewed Artifacts

| Artifact | GitHub Artifact ID | Digest | Expires |
| --- | --- | --- | --- |
| `harmonIA-windows-diagnostic-logs` | `7714638787` | `sha256:1419a5fda19ca344e9f0191e79040249c912be50b1cc8b930a4dc3e2d0376609` | 2026-06-25 |
| `harmonIA-windows-internal-installers` | `7714638513` | `sha256:1fb662dc68f80e181f75a942dd890408bacad4a8d1d07fa52a04120906effc73` | 2026-06-25 |

## Artifact Contents

Diagnostic logs artifact:

| File | Size | SHA-256 |
| --- | ---: | --- |
| `bundle-files.json` | 460 | `a68600fca7c324fa06e3c58eb4621dd2c7b5f1222af12d5fbb6415e3d53921e6` |
| `cargo-version.txt` | 37 | `ff079c1c8c4051204aeb2838a6d361b24eb1ac8e069977f4a5a6ef389934d34a` |
| `node-version.txt` | 10 | `1e818e7c43f4b13c1e913709e2425959af4b584c0bd6693bb6b5f31c29afd5e0` |
| `npm-version.txt` | 9 | `39014519a1d02a9b6e42be7478146f7d06bfe248d7f21ddfef8f4991528f5d37` |
| `python-version.txt` | 16 | `6a5d9f6462ca5dfc6788cfd216ba579fffd7875776ab9d9b35659be78858f73a` |
| `rust-version.txt` | 37 | `14abefc09d2cf8ffb51dd2244134c068b812904cb50f8d95d6661615f5c34d30` |
| `tauri-build.log` | 18,374 | `2118e3051e6e7fc80821fbf16bf781f6aaded3d1e2b89c66595d4cc840539a57` |
| `tauri-conf.json.txt` | 676 | `d7447b1ef808d181380c890827324aedfab5c6a4dfd237422706b1b6cccc1e00` |

Installer artifact:

| File | Size | SHA-256 |
| --- | ---: | --- |
| `msi/harmonIA_0.3.0_x64_en-US.msi` | 2,764,800 | `3f8d31dc6d02807623d2a6aae8a9c51becc6e14ec41049a8e110e4b30e77ca2d` |
| `nsis/harmonIA_0.3.0_x64-setup.exe` | 1,831,707 | `f9f05f8bc27de25ee3de79352453688ffedb3bcab3326fea62e1c78a0fa39d2e` |

MSI administrative extraction produced:

| File | Size | SHA-256 |
| --- | ---: | --- |
| `PFiles/harmonIA/harmonia.exe` | 8,233,984 | `875c50b89b0d8873646961ee5279bc1ef2977fcd92b2d597ccb47b628f095dcf` |

## Checklist

- [x] Artifact ZIPs were downloaded from the successful Windows diagnostic run.
- [x] Artifact ZIPs were expanded in a temporary inspection folder outside the repository.
- [x] Top-level artifact filenames were checked for `.env`, credentials, secrets, raw audio, upload folders, cache folders, and temp-folder patterns.
- [x] Diagnostic text files were reviewed for secrets and private local paths.
- [x] MSI artifact was administratively extracted without adding extracted binaries to the repository.
- [x] MSI, NSIS, and extracted app executable binary strings were scanned for secret-like values, `.env` references, local user paths, raw audio markers, and cache markers.
- [x] Workflow artifact policy was confirmed to upload only installer outputs and diagnostic files, not broad workspace folders.

## Findings

- No OpenAI-style keys, named API keys, database URLs, password assignments, secret assignments, `.env` filenames, raw audio file markers, upload-folder markers, or `.pytest_cache` markers were found.
- No local user-machine markers from the developer workstation were found in reviewed artifacts.
- The diagnostic bundle contains GitHub Actions runner build paths such as `D:\a\SoundSplit\SoundSplit\...` in the build manifest/log. This is expected CI build metadata.
- The extracted Tauri executable contains GitHub-hosted runner Rust source path strings such as `C:\Users\runneradmin\.cargo\...`. This is expected build metadata from compiled dependencies, not a private user file.
- The scan matched `publicKeyToken` in Windows manifest strings. This is assembly identity metadata, not an application secret.
- The bundled config includes the expected local diagnostic URLs, including the Tauri dev URL and local API URL behavior. No secret API target was found.
- MSI administrative extraction generated a local Windows Installer log with inspector-machine metadata. That log was not part of the CI artifact and must not be committed or published.

## Result

RLS3-001 passes for internal-only artifact review. The reviewed artifacts do not show evidence of leaked secrets, private local files, raw uploaded audio, or development cache files.

External sharing remains blocked until:

- RLS3-002 confirms installer permissions and desktop data boundaries.
- RLS3-003 records provenance, checksums, sharing policy, and unsigned-installer warnings.
- The user explicitly approves any sharing beyond the core development team.

## Handoff

```text
Agent: Linus (Release Coordinator)
Scope: RLS3-001 release artifact safety review.
Changed: Added artifact safety checklist and inspection findings for the successful Windows diagnostic build artifacts.
Validated: Downloaded and expanded both run artifacts; reviewed artifact names, diagnostic text, MSI extraction output, binary strings, checksums, and known build metadata.
Risks: NSIS installer was reviewed by artifact listing and binary-string scan only because no dedicated NSIS extraction tool was available; external sharing remains blocked by RLS3-002 and RLS3-003.
Next: Ada can proceed with RLS3-002; Linus and Grace can use these checksums and findings for RLS3-003 and SS3-004.
```
