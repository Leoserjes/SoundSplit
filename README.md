# SoundSplit

SoundSplit is a music engineering company building harmonIA, a desktop AI tool for music producers, musicians, teachers, and audio engineers.

harmonIA receives an audio file, analyzes the track, separates stems, identifies musical parts, and exports playable/editable notation artifacts such as MIDI, MusicXML, and PDF scores.

## Product Direction

The first product version is a professional desktop app powered by cloud AI:

- Desktop app: Tauri + React
- Backend API: FastAPI
- AI workers: Python + PyTorch
- Async jobs: Redis-backed queue
- Data: PostgreSQL
- File storage: S3-compatible object storage

## Repository Layout

```text
AGENTS.md        Agent operating guide
apps/
  desktop/        Tauri desktop application
  api/            FastAPI backend
workers/
  ai/             AI processing workers and audio pipeline
packages/
  contracts/      Shared schemas and API contracts
docs/
  architecture.md System architecture and flow
  agents.md       Agent responsibilities
  agent-workflows.md Agent delivery workflows
  quality-gates.md Validation levels
  task-template.md Task planning template
  mvp-roadmap.md  MVP milestones
```

## MVP Flow

```text
Audio upload
  -> API creates analysis job
  -> AI worker processes audio
  -> stems, MIDI, MusicXML, and scores are generated
  -> desktop app shows progress and downloads results
```

## Getting Started

Install JavaScript dependencies:

```bash
npm install
```

Create and install Python dependencies:

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e apps\api[test] -e workers\ai[test]
```

Run the API:

```bash
cd apps/api
..\..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Run the desktop web shell:

```bash
npm run desktop:dev
```

Run validation:

```bash
npm run desktop:build
npm run desktop:test
.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests
```

Native Tauri builds also require Rust/Cargo via rustup. The JavaScript/Tauri CLI can be installed through npm, but the native shell will not build until the Rust toolchain is available.

Run a native Tauri build:

```bash
npm --workspace apps/desktop run tauri -- build
```

On Windows, if Rust was installed but the current terminal does not yet see it, restart the terminal or add Cargo to the current session path:

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
```

If `rustup` cannot use the default user home in this environment, use a local ignored Rustup home for the project:

```powershell
$env:RUSTUP_HOME = "$PWD\.rustup"
rustup default stable
```
