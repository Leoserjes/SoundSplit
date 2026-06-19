# Agent Workflows

## Project Status Flow

Use this status flow for implementation and release-affecting cards:

1. `Ready`: Product, architecture, and acceptance criteria are clear enough to start.
2. `In Progress`: The owning developer or planning agent is actively working.
3. `QA`: Grace reviews developer tests, adds coverage where practical, and records manual gaps.
4. `Release Review`: Linus verifies release evidence only after the owning agent and QA have left handoffs.
5. `Done`: Atlas confirms required handoffs are present and unresolved findings are closed or explicitly deferred.

If the GitHub Project currently uses `In Review` instead of `QA`, treat `In Review` as the QA column until the project columns are updated. Release validation is not a replacement for developer unit tests or QA review.

## Workflow 1: Default Feature Delivery

Use this for most new harmonIA features.

1. Agent Manager opens the task, assigns owner agents, and places the card in `Ready`.
2. Product Manager writes/refines the card, user flow, business rules, and acceptance criteria.
3. Engineering Manager defines architecture impact, contracts, and technical constraints.
4. Backend Developer moves the card to `In Progress` and implements API, data, job, or worker behavior when needed, including unit tests.
5. Front-End Developer implements the desktop/frontend workflow when needed, including unit tests.
6. The implementing developer leaves a handoff and moves the card to `QA`.
7. QA reviews developer unit tests and creates or updates broader tests for affected flows.
8. QA either returns the card to `In Progress` with findings or leaves a QA handoff and moves it to `Release Review` when release validation is needed.
9. Release Coordinator includes the feature in a release candidate only after QA handoff.
10. Agent Manager checks handoffs and closes the task.

Expected output:

```text
Feature:
Requirements:
Architecture:
Backend changes:
Frontend changes:
Tests:
QA review:
Release notes:
Risks:
```

## Workflow 2: Architecture Change

Use this when product direction, folder structure, infrastructure, or data flow changes.

1. Agent Manager records the requested change.
2. Product Manager confirms the product reason and user/business impact.
3. Engineering Manager decides the technical approach.
4. Backend Developer and Front-End Developer identify implementation impact.
5. QA identifies regression areas and required QA status before implementation is considered complete.
6. Release Coordinator identifies release impact and rollback recommendation criteria after QA expectations are clear.

Expected output:

```text
Decision:
Product impact:
Technical impact:
Affected files:
Migration needed:
Validation:
Rollback recommendation:
```

## Workflow 3: Backend Feature

Use this when the change is primarily API, worker, queue, storage, or database behavior.

1. Product Manager defines behavior and acceptance criteria.
2. Engineering Manager defines boundaries and contract impact.
3. Backend Developer moves the card to `In Progress`, implements the backend change, and adds unit tests.
4. Backend Developer leaves a handoff and moves the card to `QA`.
5. QA reviews backend unit tests and adds integration scenarios.
6. Front-End Developer updates the desktop app only if the API contract changes.
7. Release Coordinator validates release readiness only after QA handoff.

Expected output:

```text
Backend feature:
API contract:
Business rules:
Implementation:
Tests:
QA review:
Release risk:
```

## Workflow 4: Frontend Feature

Use this when the change is primarily the desktop user experience.

1. Product Manager defines the user flow and acceptance criteria.
2. Engineering Manager confirms API/contract constraints.
3. Front-End Developer moves the card to `In Progress`, implements the UI/API integration, and adds unit tests.
4. Backend Developer updates endpoints only if required.
5. Front-End Developer leaves a handoff and moves the card to `QA`.
6. QA reviews frontend unit tests and adds UI or end-to-end test coverage.
7. Release Coordinator validates release readiness only after QA handoff.

Expected output:

```text
Frontend feature:
User flow:
API needs:
Implementation:
Tests:
QA review:
Release risk:
```

## Workflow 5: AI Pipeline Feature

Use this when adding real audio processing behavior.

1. Product Manager confirms the musician/producer value.
2. Engineering Manager defines runtime, dependency, and architecture constraints.
3. Backend Developer moves the card to `In Progress`, implements worker/API integration, and adds unit tests.
4. Backend Developer leaves a handoff and moves the card to `QA`.
5. QA reviews unit tests and defines fixture-based tests and expected artifacts.
6. Front-End Developer displays new progress or artifact states when needed, then returns the card to `QA` for changed UI behavior.
7. Release Coordinator confirms dependency and runtime readiness only after QA handoff.

Expected output:

```text
Pipeline step:
Input:
Output artifacts:
Model/library dependency:
Runtime considerations:
Tests:
QA review:
Release risk:
```

## Workflow 6: Bug Fix

Use this when correcting broken behavior.

1. Agent Manager assigns the owner agent.
2. QA reproduces or defines the failing behavior when possible.
3. Product Manager confirms expected behavior if ambiguous.
4. Engineering Manager reviews technical risk if the fix touches architecture.
5. Backend Developer or Front-End Developer moves the card to `In Progress`, implements the fix, and adds a unit test.
6. The implementing developer leaves a handoff and moves the card to `QA`.
7. QA reviews the unit test and adds a regression test.
8. Release Coordinator decides whether the fix belongs in a patch release only after QA handoff.

Expected output:

```text
Bug:
Expected behavior:
Root cause:
Fix:
Regression test:
QA review:
Release impact:
```

## Workflow 7: Dependency Installation

Use this before installing or upgrading packages.

1. Product Manager confirms the dependency supports the product goal.
2. Engineering Manager confirms technical fit and alternatives.
3. Backend Developer or Front-End Developer moves the card to `In Progress` and installs the dependency.
4. The implementing developer leaves a handoff and moves the card to `QA`.
5. QA records validation commands.
6. Release Coordinator reviews lockfiles and build output only after QA handoff.

Expected output:

```text
Dependency:
Reason:
Alternatives considered:
Install command:
Validation:
Release risk:
```

## Workflow 8: Release

Use this for each release candidate.

1. Product Manager confirms the feature scope.
2. Engineering Manager confirms technical readiness.
3. QA confirms each included implementation card has a QA handoff or an explicit deferral.
4. QA runs the required release-candidate test suite.
5. Release Coordinator prepares release notes and tags/builds the release after QA signoff.
6. Release Coordinator runs post-release validation.
7. If validation fails, Release Coordinator creates a failure document and suggests rollback according to the rollback policy.
8. Agent Manager archives the release handoff.

Expected output:

```text
Release:
Included features:
Test results:
Known risks:
Rollback plan:
Rollback suggestion:
Post-release validation:
Incident note:
```
