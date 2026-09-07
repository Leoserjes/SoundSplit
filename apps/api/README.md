# SoundSplit API

FastAPI service for jobs, local uploads, artifact downloads, and cited knowledge search. Follow the repository [setup](../../README.md#getting-started), which installs the required local knowledge package.

Run from the repository root to keep `.env`, SQLite, and storage paths consistent:

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Inspect `/docs` and `/openapi.json` for route contracts. See [current architecture](../../docs/architecture.md) and [manual validation](../../docs/quality-gates.md).
