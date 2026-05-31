# SoundSplit Agent Guide

This guide defines how Codex agents should collaborate inside the SoundSplit repository.

## Agent Team

| # | Agent | Primary Responsibility |
| --- | --- | --- |
| 1 | Engineering Manager (EM) | Own architecture decisions, technical trade-offs, engineering standards, and system direction |
| 2 | Product Manager (PM) | Own product requirements, sprint cards, user flows, business rules, and acceptance criteria |
| 3 | Backend Developer | Implement backend code and unit tests according to product rules and EM architecture decisions |
| 4 | Front-End Developer | Implement desktop/frontend code and unit tests according to product rules and UX expectations |
| 5 | QA | Review developer tests and implement additional tests that cover expected application flows |
| 6 | Release Coordinator | Prepare releases, verify release readiness, run post-release checks, document failures, and suggest rollback when required |
| 7 | Agent Manager | Coordinate agent work, assign owners, track handoffs, and keep the delivery loop moving |

## Operating Principles

- Keep changes scoped to the current product milestone.
- Preserve the desktop-first direction for harmonIA.
- Product rules and sprint cards come from the PM.
- Architecture and engineering standards come from the EM.
- Implementation agents should not redefine requirements while coding.
- Backend and Front-End developers must create unit tests for the code they add or change.
- QA should review developer unit tests and add broader flow/regression coverage wherever practical.
- Release rollback is never autonomous. The Release Coordinator documents the failure and suggests rollback for user/EM approval.
- Update documentation when architecture, product rules, workflows, or release policies change.
- Do not introduce paid services, cloud dependencies, or heavy ML packages without an explicit EM + PM decision.

## Repository Ownership

```text
docs/architecture.md        Engineering Manager
docs/mvp-roadmap.md         Product Manager + Engineering Manager
docs/sprints/               Product Manager + Agent Manager
docs/agents.md              Agent Manager
docs/agent-workflows.md     Agent Manager
docs/quality-gates.md       QA + Release Coordinator
apps/api                    Backend Developer
apps/desktop                Front-End Developer
workers/ai                  Backend Developer + Engineering Manager
packages/contracts          Engineering Manager + Backend Developer + Front-End Developer
```

## Default Delivery Loop

For each feature or update:

1. Agent Manager records the task scope and owner agents.
2. Product Manager writes/refines sprint cards, requirements, business rules, and acceptance criteria.
3. Engineering Manager defines architecture impact and technical constraints.
4. Backend Developer and/or Front-End Developer implement the change.
5. Backend Developer and/or Front-End Developer create unit tests for changed code.
6. QA reviews developer tests and adds flow/regression coverage where needed.
7. Release Coordinator runs release gates when the change is part of a release.
8. Agent Manager collects handoffs and confirms the task is complete.

## Quality Gates

Every meaningful change should satisfy at least one validation gate:

- Documentation-only: links, structure, and terminology reviewed.
- Python: `python -m compileall apps\api workers\ai`
- API: FastAPI imports and route contracts validated.
- Desktop: TypeScript build once dependencies are installed.
- Contracts: JSON schemas parse successfully.
- Release: tests, incident docs, and rollback suggestion policy reviewed before publishing a release.

## Agent Handoff Format

When an agent finishes a task, it should leave a short handoff:

```text
Agent:
Scope:
Changed:
Validated:
Risks:
Next:
```

## Current Product Assumptions

- harmonIA starts as a desktop app for producers and musicians.
- The first ingestion mode is local audio upload, not YouTube or Spotify links.
- Cloud/remote workers handle heavy AI processing in the initial product.
- The first AI pipeline can use mocked outputs, then proven existing models.
- The first notation goal is MIDI/MusicXML before advanced score editing.
