# Sprint 05: v0.6.0 Worker Pipeline And Audio Normalization

Status: Draft

## Sprint Summary

Duration: 14 calendar days
Planned start: 2026-07-18
Planned end: 2026-08-01
Release target: `v0.6.0`
Sprint owner: Maestro - Product Manager
Delivery coordinator: Atlas - Agent Manager

## Central Objective

Connect durable API jobs to a first worker execution path and produce the first processed audio artifact. The sprint should introduce worker handoff, progress/error updates, audio metadata extraction, and a normalized audio output without adding stem separation, transcription, or heavy ML packages.

## Scope

In:

- Worker execution contract.
- Queue or local worker handoff decision.
- Job status transitions from `queued` to `processing`, `completed`, or `failed`.
- Worker progress/error reporting.
- Audio metadata extraction for uploaded source files.
- First normalized audio artifact.
- Desktop progress refresh and failure states.
- QA report and release notes for `v0.6.0`.

Out:

- Stem separation.
- MIDI transcription.
- MusicXML or PDF generation.
- Heavy ML packages.
- Offline model packaging.
- Public installer distribution.

## Product Rules

- The user-facing flow remains upload first, then process.
- The desktop app must clearly show when processing is pending, active, complete, or failed.
- If audio tooling only supports a subset of currently accepted formats at first, the limitation must be explicit before implementation.
- Normalized output must be described as a technical processing artifact, not as separated stems or notation.

## Proposed Technical Decisions For Review

- Decide whether Sprint 05 uses Redis-backed queueing or a simpler local worker handoff before implementation.
- Choose lightweight audio tooling before adding dependencies.
- Prefer a worker boundary that can later host stem separation and transcription without rewriting job orchestration.
- Keep processing artifacts stored through the Sprint 04 artifact service.

## Draft Cards

### SS5-001: Decide Worker Runtime And Audio Tooling

Agent Owner: Ada
Supporting: Turing, Maestro, Grace
Status: Draft

Acceptance Criteria:

- Worker execution approach is documented.
- Audio tooling options are compared for supported formats, install cost, licensing, and reliability.
- EM and PM approve any new system or Python dependency.
- Unsupported format behavior is documented if necessary.

### SS5-002: Add Worker Handoff Contract

Agent Owner: Turing
Supporting: Ada, Grace
Status: Draft

Acceptance Criteria:

- API can enqueue or hand off durable jobs to the worker path.
- Worker receives source artifact metadata from Sprint 04.
- Job status changes are persisted.
- Tests cover successful handoff and failure handling.

### SS5-003: Add Worker Progress And Error Reporting

Agent Owner: Turing
Supporting: Pixel, Grace
Status: Draft

Acceptance Criteria:

- Worker can report `processing`, `completed`, and `failed` states.
- Error messages are safe, short, and useful.
- API job responses expose the status needed by the desktop app.
- Tests cover status transitions.

### SS5-004: Extract Audio Metadata

Agent Owner: Turing
Supporting: Ada, Grace
Status: Draft

Acceptance Criteria:

- Worker records duration, channels, sample rate, and detected input format when supported.
- Unsupported or unreadable files fail gracefully.
- Metadata is attached to the job or artifact record according to the approved contract.
- Tests use small deterministic fixtures.

### SS5-005: Generate Normalized Audio Artifact

Agent Owner: Turing
Supporting: Ada, Grace
Status: Draft

Acceptance Criteria:

- Worker generates one normalized audio artifact for supported input.
- Artifact metadata is stored through the Sprint 04 artifact boundary.
- Failures do not corrupt source upload records.
- Tests cover success and failure paths.

### SS5-006: Update Desktop Progress And Failure States

Agent Owner: Pixel
Supporting: Maestro, Turing, Grace
Status: Draft

Acceptance Criteria:

- Desktop displays queued, processing, completed, and failed states.
- Desktop refreshes job state without overwhelming the API.
- Normalized audio artifact availability is visible.
- Frontend tests cover progress and failure UI.

### SS5-007: QA Review And Worker Flow Regression Coverage

Agent Owner: Grace
Supporting: Turing, Pixel, Ada, Linus
Status: Draft

Acceptance Criteria:

- QA report records automated and manual validation.
- Worker handoff, status updates, metadata extraction, and normalized artifact paths are covered.
- Known format limitations are documented.
- Regression risk from Sprint 04 durable storage is reviewed.

### SS5-008: Release v0.6.0

Agent Owner: Linus
Supporting: Atlas, Grace, Ada, Maestro
Status: Draft

Acceptance Criteria:

- Release notes identify worker pipeline behavior and limitations.
- Validation results are recorded.
- Rollback suggestion criteria include worker failures and artifact corruption.
- User approval is received before tagging.

## Sprint Risks

- Audio tooling may require system dependencies that complicate Windows distribution.
- MP3 and FLAC handling can differ across libraries and platforms.
- Queue integration may reveal infrastructure gaps from local development setup.
- Worker failures must not leave jobs stuck in ambiguous states.

## Definition Of Ready For Sprint Start

- Sprint 04 durable job/artifact boundary is complete or explicitly scoped down.
- EM and PM approve the worker runtime and audio tooling decision card.
- Atlas creates GitHub issue cards from the approved draft.

## Definition Of Done

- Approved cards are Done or explicitly Deferred.
- A worker path produces at least one normalized artifact or documents a blocking decision.
- QA report and release notes are complete.
- User approves any release tag.
