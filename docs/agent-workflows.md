# Agent Workflows

## Workflow 1: Default Feature Delivery

Use this for most new harmonIA features.

1. Agent Manager opens the task and assigns owner agents.
2. Product Manager writes/refines the card, user flow, business rules, and acceptance criteria.
3. Engineering Manager defines architecture impact, contracts, and technical constraints.
4. Backend Developer implements API, data, job, or worker behavior when needed, including unit tests.
5. Front-End Developer implements the desktop/frontend workflow when needed, including unit tests.
6. QA reviews developer unit tests and creates or updates broader tests for affected flows.
7. Release Coordinator includes the feature in a release candidate when ready.
8. Agent Manager checks handoffs and closes the task.

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
5. QA identifies regression areas.
6. Release Coordinator identifies release impact and rollback recommendation criteria.

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
3. Backend Developer implements the backend change and unit tests.
4. QA reviews backend unit tests and adds integration scenarios.
5. Front-End Developer updates the desktop app only if the API contract changes.
6. Release Coordinator validates release readiness.

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
3. Front-End Developer implements the UI, API integration, and unit tests.
4. Backend Developer updates endpoints only if required.
5. QA reviews frontend unit tests and adds UI or end-to-end test coverage.
6. Release Coordinator validates release readiness.

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
3. Backend Developer implements worker/API integration and unit tests.
4. QA reviews unit tests and defines fixture-based tests and expected artifacts.
5. Front-End Developer displays new progress or artifact states.
6. Release Coordinator confirms dependency and runtime readiness.

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
5. Backend Developer or Front-End Developer implements the fix and unit test.
6. QA reviews the unit test and adds a regression test.
7. Release Coordinator decides whether the fix belongs in a patch release.

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
3. Backend Developer or Front-End Developer installs the dependency.
4. QA records validation commands.
5. Release Coordinator reviews lockfiles and build output.

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
3. QA runs the required test suite.
4. Release Coordinator prepares release notes and tags/builds the release.
5. Release Coordinator runs post-release validation.
6. If validation fails, Release Coordinator creates a failure document and suggests rollback according to the rollback policy.
7. Agent Manager archives the release handoff.

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
