# WebView2 Strategy For Windows Distribution

Status: Approved for Sprint 03 internal diagnostic builds
Owner: Ada - Engineering Manager
Supporting: Maestro - Product Manager, Linus - Release Coordinator
Last reviewed: 2026-06-18

## Decision

For Sprint 03, harmonIA should keep Tauri's default Windows WebView2 installation behavior: `downloadBootstrapper`.

This means the installer remains small and downloads the Evergreen WebView2 Runtime bootstrapper only when WebView2 is missing. This is acceptable for Sprint 03 because installer work is diagnostic/internal only, harmonIA is a connected desktop app, and public/offline distribution is explicitly out of scope.

No `tauri.conf.json` change is required for Sprint 03 because `apps/desktop/src-tauri/tauri.conf.json` does not override `bundle.windows.webviewInstallMode`.

## Rationale

- harmonIA currently targets connected desktop use, not offline installation.
- Windows 11 includes WebView2, and many Windows 10 devices already have the Evergreen runtime.
- Tauri's default keeps installer artifacts small and avoids early packaging rework.
- Evergreen WebView2 receives runtime/security updates without harmonIA owning a fixed browser runtime update cycle.
- Sprint 03 artifacts remain internal diagnostics until release-safety cards and user approval allow broader sharing.

## Option Comparison

| Option | Tauri value | Installer size impact | Network requirement | Maintenance impact | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Downloaded Evergreen bootstrapper | `downloadBootstrapper` | Smallest installer | Requires internet when runtime is missing | Low; Evergreen runtime updates itself | Use for Sprint 03 internal diagnostic builds |
| Embedded Evergreen bootstrapper | `embedBootstrapper` | Adds about 1.8 MB | Requires internet when runtime is missing | Low; avoids downloading the bootstrapper itself | Revisit if downloader UX or CDN dependency is a problem |
| Evergreen offline installer | `offlineInstaller` | Adds about 127 MB | No internet needed to install runtime | Low runtime maintenance, larger artifacts | Revisit for offline or less technical internal testers |
| Fixed runtime | `fixedRuntime` | Adds about 180 MB | No runtime install dependency | High; harmonIA owns runtime patch/update cadence | Do not use before a specific compatibility requirement |
| Skip WebView2 install | `skip` | Small | No installer attempt | Risky; app will not work without runtime | Do not use for tester builds |

## Clean-Machine Validation Notes

Clean-machine validation for Sprint 03 should record:

- Windows version.
- Whether WebView2 was already installed.
- Whether the machine had internet access during install.
- Installer type tested: MSI, NSIS, or both.
- Any user-visible WebView2 prompt, download delay, or installation failure.
- Whether harmonIA launches after installation.
- Whether the connected API unavailable state is still understandable after launch.

For Sprint 03, a clean-machine failure caused only by missing internet/WebView2 should not be treated as a product runtime failure. It should be recorded as a distribution limitation of the selected strategy.

## Release Notes Language

Use language like this for `v0.4.0`:

```text
Windows installer diagnostics use Tauri's default WebView2 downloaded bootstrapper strategy. Installer artifacts remain internal-only. Clean machines without WebView2 may need internet access during installation unless a future sprint switches to an offline WebView2 installer mode.
```

## Revisit Triggers

Revisit this decision when any of the following become true:

- Installer artifacts are shared with non-developer testers.
- Testers need offline installation.
- Clean-machine validation shows confusing WebView2 installer UX.
- Target users include locked-down or managed Windows environments.
- Public distribution begins.
- Code signing and release channels are ready.
- The app requires a specific WebView2 runtime feature version.

## Current Follow-Ups

- SS3-003 should keep Windows CI artifacts marked as internal diagnostics.
- SS3-004 should test and record WebView2 presence and internet availability.
- SS3-006 should mention that code signing is separate from WebView2 runtime distribution.
- RLS3-003 should block external sharing until installer provenance, unsigned warnings, and WebView2 limitations are documented.
