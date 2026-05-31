# Sprint 03 Backlog: Connected Desktop Distribution

Status: Backlog for planning

## Direction

Prepare harmonIA for reliable Windows distribution as a connected desktop app. The Tauri desktop client will call a remote FastAPI backend. Offline AI processing is explicitly deferred.

## Candidate Cards

### SS3-001: Add Environment-Aware API Configuration

- Define development, staging, and production API URLs.
- Keep HTTP integration as the primary desktop path.
- Add clear offline/connection error messaging.

### SS3-002: Create Single-Command Developer Startup

- Start FastAPI and desktop dev shell through one documented command.
- Avoid reliance on shell-specific `PATH` mutations.
- Document Rust setup separately from normal app startup.

### SS3-003: Add Windows CI Build

- Build MSI and NSIS installers in a clean Windows CI environment.
- Run frontend, backend, and Rust validation gates.
- Upload build artifacts for review.

### SS3-004: Validate Clean-Machine Installation

- Test NSIS/MSI installation on Windows Sandbox or a clean VM.
- Confirm desktop launch without development dependencies.
- Confirm remote API connectivity behavior.

### SS3-005: Decide WebView2 Strategy

- Compare downloaded bootstrapper, embedded bootstrapper, and offline installer modes.
- Choose the release default based on installer size and target audience.

### SS3-006: Plan Windows Code Signing

- Document certificate requirements.
- Estimate cost and release workflow impact.
- Add signing only when distribution leaves internal testing.

## Explicitly Deferred

- Offline AI processing.
- Local PyTorch model distribution.
- Python/FastAPI sidecar packaging.
- Automatic model downloads.
