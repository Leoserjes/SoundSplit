# Manual Validation

Validation is run manually in this phase so each step can be inspected and understood. No new CI configuration is required. Shared ownership, QA handoffs, and release rules live in [AGENTS.md](../AGENTS.md).

Run commands individually from the repository root, after following the [setup](../README.md#getting-started). Inspect the result and exit code before continuing; record failures rather than reporting unchecked steps as passed.

| Change | Manual checks | Purpose |
| --- | --- | --- |
| Documentation | Review local links, commands, terminology, and current behavior | Prevent stale or misleading guidance |
| Developer startup | `npm run dev:check` | Check launcher behavior |
| Desktop | `npm run desktop:test`, then `npm run desktop:build` | Check behavior and TypeScript/build compatibility |
| Python packages | Command below | Check API, worker, and knowledge regression coverage |
| Contracts | Parse schemas and compare with API responses/OpenAPI | Detect contract drift; parsing alone does not prove compatibility |
| Release candidate | All relevant checks plus native build and manual installation/flow checks | Verify the delivered application |

## Python Regression Checks

```powershell
.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests packages\knowledge\tests
```

Unit tests do not establish that a live Notion synchronization, PostgreSQL search, or embedding service works. When changing retrieval integration, also exercise the [retrieval setup and query flow](knowledge-retrieval.md), documenting the environment and any unavailable services.

## Contract Syntax

```powershell
Get-Content packages\contracts\job.schema.json -Raw | ConvertFrom-Json | Out-Null
Get-Content packages\contracts\upload.schema.json -Raw | ConvertFrom-Json | Out-Null
```

## Manual Application Flow

1. Run `npm run dev` and check `/health` and `/docs` on the API.
2. Submit a small local WAV, MP3, or FLAC file. Confirm the returned job ID, `queued` status, and placeholder artifact metadata.
3. Use `/docs` to retrieve the job, list artifacts, and download an artifact using its returned URI. Placeholder files do not demonstrate real audio processing.
4. Restart the API from the same working directory and confirm the job and upload persist.
5. Check unsupported extension and empty-upload errors. Review regression coverage for oversized uploads.
6. Record UI gaps explicitly: automatic job polling and download buttons are not currently implemented.

Use disposable local inputs. Runtime files belong in ignored storage paths; do not commit generated uploads, databases, or artifacts.

## Release Evidence

Run the native build when validating a desktop release:

```powershell
npm --workspace apps/desktop run tauri -- build
```

Follow the relevant [distribution procedures](distribution/). Record the application version, source commit, relevant component versions, environment, commands and results, manual checks, skipped checks, artifact hashes, and known limitations in the release Issue/PR or GitHub Release. Components may have different versions. A successful build does not replace installation testing.

Record post-release failures in an Issue. Recommend rollback with impact and recovery risks; obtain user/EM approval before executing it.
