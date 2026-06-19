# Windows Code Signing Plan

Status: Approved planning decision for Sprint 03
Owner: Linus - Release Coordinator
Supporting: Ada - Engineering Manager, Maestro - Product Manager
Last reviewed: 2026-06-19

## Sprint 03 Decision

Keep Windows code signing deferred for `v0.4.0`.

Do not purchase certificates or signing services in Sprint 03. Do not add signing secrets, do not modify CI secrets, and do not change the Windows diagnostic build workflow to sign artifacts.

When SoundSplit is ready to distribute harmonIA beyond internal diagnostic testing, use Azure Artifact Signing as the first candidate if eligibility, cost, and account setup are acceptable. Keep traditional OV certificates and EV certificates as alternatives if Azure Artifact Signing is not available for the publisher identity or release channel.

## Why This Matches The Current Release Risk

This decision avoids installer rework while the team is still validating packaging, WebView2 behavior, clean-machine install behavior, artifact safety, and release provenance.

Signing is a distribution trust and publisher identity decision. It does not replace artifact safety review, clean-machine QA, or release provenance checks. Keeping `v0.4.0` unsigned and internal-only prevents the team from committing to a certificate provider, paid Azure resource, hardware token, or CI secret model before EM, PM, and user approval.

## Option Comparison

| Option | Fit For SoundSplit | Cost Notes | Eligibility And Setup | Risks | Sprint 03 Decision |
| --- | --- | --- | --- | --- | --- |
| Microsoft Store signing | Best if the release strategy moves to Microsoft Store MSIX distribution. Microsoft re-signs Store MSIX packages. MSI/EXE Store submissions still require publisher signing. | Store MSIX signing is handled by Microsoft; other Store costs or account requirements must be checked before a release-channel decision. | Requires Store packaging/listing decisions and Partner Center workflow. This is a product/channel decision, not only a release engineering decision. | Could force packaging and release-channel work before harmonIA is ready. Current Sprint 03 artifacts are MSI/NSIS diagnostics, not Store submissions. | Defer. Revisit when PM chooses a public distribution channel. |
| Azure Artifact Signing | Preferred first candidate for future non-Store distribution if SoundSplit is eligible. It is managed, CI-friendly, uses FIPS 140-2 Level 3 private-key protection, and avoids local private-key handling. | Microsoft Windows app guidance lists Azure Artifact Signing at about `$9.99/month`; the Azure pricing page exposes Basic/Premium tiers and says pricing is only an estimate. Current research notes recorded Basic around `$9.99/month` and Premium around `$99.99/month`; verify before purchase. | Requires a paid Azure subscription, Artifact Signing account, identity validation, and certificate profile. Public Trust availability depends on publisher type and region. | Adds paid Azure dependency, identity validation lead time, and future CI authentication. SmartScreen reputation still builds over time for new files. Service status, public preview or GA terms, and pricing must be checked again before approval. | Defer purchase/setup. Prefer later if EM, PM, and user approve cost, region eligibility, and CI secret policy. |
| Traditional OV certificate | Fallback for non-Store distribution when Azure Artifact Signing is not available or a customer requires a traditional CA. | Microsoft guidance lists typical OV cost around `$150-300/year`; actual CA quotes and renewal terms must be verified. Certificates issued on or after 2026-03-01 cannot exceed 460 days of validity under CA/B Forum requirements. | Requires CA identity validation and protected private-key storage, usually hardware token or managed HSM. | More operational handling than Azure Artifact Signing; token/HSM logistics can slow CI and releases. SmartScreen reputation still builds over time. | Keep as alternative. No purchase in Sprint 03. |
| EV certificate | Only consider if enterprise procurement or a specific trust requirement justifies it. | Microsoft guidance lists EV at about `$400+/year`; actual CA quotes must be verified. The same 460-day maximum validity applies for certificates issued on or after 2026-03-01. | Requires stricter identity validation and protected key storage. | Microsoft guidance says EV no longer provides the old instant SmartScreen bypass advantage; cost and friction are higher than OV. | Do not prefer. Keep as exceptional fallback. |
| Unsigned internal diagnostics | Current Sprint 03 path for CI-generated MSI/NSIS artifacts. | No signing cost. | No certificate, service, account, or secret setup. | Windows SmartScreen or enterprise policy may warn or block. Not acceptable for public distribution. | Use for `v0.4.0` internal diagnostics only. External sharing remains blocked until release gates approve otherwise. |

## Cost, Eligibility, And Approval Notes

- All prices are planning estimates as of this review and must be verified on official pricing pages or vendor quotes before purchase.
- Azure Artifact Signing requires a paid Azure subscription; Microsoft FAQ says free, trial, and sponsored Azure subscriptions are unsupported.
- Azure Artifact Signing Public Trust eligibility must be checked against the publisher identity and country/region before approval.
- Traditional OV/EV planning must account for CA/B Forum private-key protection requirements and the 460-day maximum certificate validity period for certificates issued on or after 2026-03-01.
- Signing should not begin until the team has a confirmed publisher legal identity, signing owner, budget owner, renewal owner, and incident/revocation owner.
- SoundSplit currently builds Windows diagnostic artifacts on GitHub `windows-latest`. If a future workflow cross-compiles Windows installers from Linux or macOS, Tauri documents that installer signing needs an external signing tool.

Required approval before any purchase or implementation:

- Ada - Engineering Manager: signing architecture, CI trust boundary, secret handling, and rollback impact.
- Maestro - Product Manager: distribution channel, tester/user messaging, and whether signed public distribution is in scope.
- User/business owner: paid service or certificate purchase, legal identity validation, and authorization to create external accounts.
- Linus - Release Coordinator: release workflow updates, artifact verification, timestamp/signature verification, and release-note wording.

## CI And Secret Impact

No CI or secret changes are approved by this Sprint 03 plan.

Future signing work must follow this no-secret policy:

- Do not commit certificates, private keys, client secrets, tenant IDs, signing metadata with sensitive values, or local signing files.
- Do not place signing secrets in docs, release notes, logs, artifact manifests, or uploaded diagnostics.
- Prefer short-lived or federated CI authentication when the selected provider supports it.
- If provider-specific secrets are required, store them only in GitHub Actions secrets or an approved secret manager after EM, PM, and user approval.
- Restrict signing workflow permissions to the minimum required for checkout, build, signing, and artifact upload.
- Keep the unsigned diagnostic workflow separate from any future signed release workflow unless Ada approves a merge.
- Verify signed output with SignTool before publishing, including signature trust and timestamp evidence, and record verification in release evidence.

Potential future implementation tasks, after approval:

- Add a signed Windows release workflow separate from the diagnostic workflow.
- Configure Tauri Windows signing using either Azure Artifact Signing, a custom sign command, or a provider-specific signing path.
- Add signature verification and timestamp checks to release gates.
- Update artifact retention and release provenance docs for signed artifacts.
- Add revocation, key rotation, and incident response notes to release policy.

## Release Notes Language For v0.4.0

Use this language in `v0.4.0` release notes:

```text
Windows installer artifacts for v0.4.0 are unsigned internal diagnostics. Code signing is intentionally deferred while the team validates installer safety, clean-machine installation, WebView2 behavior, and release provenance. Windows SmartScreen or enterprise policy may warn or block unsigned artifacts. Do not redistribute these artifacts externally until a signing decision, release safety review, provenance record, and explicit approval are complete.
```

## Sources Reviewed

- Microsoft Windows app code-signing options: https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options
- Microsoft Azure Artifact Signing product page: https://azure.microsoft.com/en-us/products/artifact-signing
- Microsoft Azure Artifact Signing documentation: https://learn.microsoft.com/en-us/azure/artifact-signing/
- Microsoft Azure Artifact Signing setup quickstart: https://learn.microsoft.com/en-us/azure/artifact-signing/quickstart
- Microsoft Azure Artifact Signing pricing: https://azure.microsoft.com/en-us/pricing/details/artifact-signing/
- Microsoft Artifact Signing FAQ: https://learn.microsoft.com/en-us/azure/artifact-signing/faq
- Microsoft SignTool docs: https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool
- Tauri v2 Windows signing docs: https://v2.tauri.app/distribute/sign/windows/
- Tauri v2 Windows installer docs: https://v2.tauri.app/distribute/windows-installer/
- CA/B Forum code signing requirements: https://cabforum.org/working-groups/code-signing/requirements/

## Linus Handoff

```text
Agent: Linus (Release Coordinator)
Scope: SS3-006 Windows code-signing planning for Sprint 03.
Changed: Added the Windows code-signing plan, option comparison, approval gates, no-secret policy, CI impact notes, and v0.4.0 release-note language.
Validated: Reviewed Microsoft, Tauri, Azure Artifact Signing, SignTool, and CA/B Forum documentation; confirmed no signing implementation, purchases, CI secret changes, or workflow secret changes were added.
Risks: Azure Artifact Signing eligibility, final pricing, identity validation lead time, SmartScreen reputation behavior, and traditional certificate private-key logistics still need approval-time verification.
Next: Keep v0.4.0 artifacts unsigned and internal-only; revisit signing when external distribution becomes a PM-approved release goal and EM/user approval exists for paid services and CI secret handling.
```
