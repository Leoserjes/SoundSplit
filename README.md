# SoundSplit

SoundSplit is a music engineering company building harmonIA, a desktop AI tool for music producers, musicians, teachers, and audio engineers.

harmonIA is a desktop music analysis application under development. The current implementation accepts local audio uploads, persists jobs in SQLite, stores files locally, and returns placeholder artifacts. Real separation, transcription, and PDF export are future capabilities.

## Repository Layout

- `apps/desktop`: Tauri + React desktop shell.
- `apps/api`: FastAPI jobs, upload, download, and knowledge search endpoints.
- `workers/ai`: audio pipeline stub; not yet connected to a job queue.
- `packages/contracts`: shared JSON schemas.
- `packages/knowledge`: Notion ingestion and cited retrieval.
- `docs`: versioned technical documentation and operating procedures.
- `.github/ISSUE_TEMPLATE`: reusable task template.

## Documentation and Planning

[GitHub Projects](https://github.com/users/Leoserjes/projects/1) and linked [Issues](https://github.com/Leoserjes/SoundSplit/issues) own backlog, priorities, sprint scope, status, acceptance criteria, and handoffs. Do not duplicate active planning in Markdown.

Keep setup instructions, current [architecture](docs/architecture.md), [manual validation](docs/quality-gates.md), and reusable distribution procedures with the code. [AGENTS.md](AGENTS.md) owns shared agent rules; individual agent files add role-specific context. The Notion Knowledge Base owns curated knowledge consumed by retrieval; it is not a second sprint board.

Components may have independent versions. The final application has its own release version, reflected in the Tauri application configuration. Release evidence should identify the application version, source commit, and relevant component versions. Do not bump unrelated components simply to make their versions match.

## Getting Started

Install JavaScript dependencies:

```bash
npm ci
```

From the repository root, create the virtual environment and install all required local Python packages:

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e "packages/knowledge[postgres,test]" -e "apps/api[test]" -e "workers/ai[test]"
```

The API imports the local knowledge package, so it is included above. Audio development does not require running PostgreSQL or embeddings. Install the optional embedding dependencies only when working on retrieval:

```bash
.venv\Scripts\python.exe -m pip install -e "packages/knowledge[postgres,embeddings,test]" -e "apps/api[test]" -e "workers/ai[test]"
```

Setup, synchronization, query examples, and trust rules are documented in
[SoundSplit Knowledge Retrieval](docs/knowledge-retrieval.md).

Run the API and desktop web shell together:

```bash
npm run dev
```

This starts the API at `http://127.0.0.1:8000` and the desktop web shell at `http://127.0.0.1:1420`. Press `Ctrl+C` in the terminal to stop both processes. The command uses the repository `.venv` Python path and the existing npm desktop workspace script.

Run the API separately:

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Run the desktop web shell separately:

```bash
npm run desktop:dev
```

### Desktop API Configuration

The desktop web shell defaults to the local API at `http://127.0.0.1:8000`.

Use these Vite environment variables when validating another connected API target:

```bash
VITE_API_ENVIRONMENT=development
VITE_API_BASE_URL=http://127.0.0.1:8000
```

`VITE_API_ENVIRONMENT` accepts `development`, `staging`, or `production`. `VITE_API_BASE_URL` takes precedence when set and trailing slashes are removed before requests are sent. Staging and production URLs can remain placeholders until hosted API environments exist.

Run the [manual validation checklist](docs/quality-gates.md) from the repository root. Record results in the related Issue or PR.

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
