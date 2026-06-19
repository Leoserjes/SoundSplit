# Quality Gates

Quality gates keep harmonIA moving quickly without losing structure.

## Gate Levels

| Level | When to Use | Required Checks | Owner |
| --- | --- | --- | --- |
| L0 Docs | Documentation-only changes | Review links, headings, and terminology | Agent Manager |
| L1 Structure | New files, schemas, or app shells | JSON parsing, Python compile checks where relevant | EM + QA |
| L2 Feature | Working API/UI behavior | Developer unit tests, developer handoff, QA review in the `QA` column, smoke checks, contract alignment, manual path check | Developer + QA |
| L3 Integration | API + desktop + worker flow | End-to-end job flow, storage/queue behavior, regression review, QA handoff before release review | QA + EM |
| L4 Release | User-facing build or release candidate | Prior developer and QA handoffs, full build, test suite, release notes, rollback recommendation criteria | Release Coordinator |
| L5 Post-Release | Published release validation | Post-release tests, incident note on failure, rollback suggestion when needed | Release Coordinator |

## Gate Ownership Rule

Implementation cards must have separate developer and QA evidence before they are marked `Done`.

- Developers own implementation and unit tests, then move the card to `QA`.
- QA owns independent review, regression coverage, and manual-gap documentation.
- Release Coordinator owns release readiness after QA, and should not backfill missing developer or QA validation during release prep.
- If QA finds issues, the card returns to `In Progress` with clear findings instead of moving forward.

## Current Lightweight Commands

Run these before dependencies are installed:

```powershell
Get-Content package.json | ConvertFrom-Json | Out-Null
Get-Content apps\desktop\package.json | ConvertFrom-Json | Out-Null
Get-Content apps\desktop\src-tauri\tauri.conf.json | ConvertFrom-Json | Out-Null
Get-Content packages\contracts\job.schema.json | ConvertFrom-Json | Out-Null
python -m compileall apps\api workers\ai
```

After dependencies are installed, add:

```powershell
npm run desktop:build
npm run desktop:test
.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests
```

For the API, add environment-specific commands once the Python package manager is chosen.

## QA Review Checklist

- Does every requirement have acceptance criteria?
- Did the developer add unit tests for changed code?
- Did the developer leave a handoff before moving the card to `QA`?
- Did QA review those unit tests?
- Are happy paths covered?
- Are failure paths covered for risky flows?
- Are regression tests added for fixed bugs?
- Are tests repeatable without hidden local state?
- Are unautomated checks documented?
- Did QA leave a handoff before the card moved to release review or Done?

## EM Review Checklist

- Does the change match the desktop-first product direction?
- Are contracts and implementation naming aligned?
- Does the job lifecycle still make sense?
- Are new dependencies justified?
- Are architecture boundaries preserved?

## Release Checklist

- Did the PM confirm release scope?
- Did the EM confirm technical readiness?
- Do included implementation cards have developer and QA handoffs?
- Did QA run the required test suite before release prep?
- Are release notes prepared?
- Are rollback recommendation criteria documented?
- Were post-release checks run?
- If a post-release check failed, was an incident note created?
- If the release is unsafe, did the Release Coordinator suggest rollback instead of executing it autonomously?
