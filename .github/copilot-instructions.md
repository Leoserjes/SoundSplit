# SoundSplit Copilot Instructions

Use English for repository work, handoffs, summaries, and planning.

Follow the project operating model in [AGENTS.md](../AGENTS.md). The stable agent identities are Ada, Maestro, Turing, Pixel, Grace, Linus, and Atlas.

Core product assumptions:

- harmonIA is a desktop-first app for producers, musicians, teachers, and audio engineers.
- The first ingestion mode is local audio upload.
- Heavy AI processing belongs in backend/worker infrastructure first, not in the desktop client.
- The first notation target is MIDI/MusicXML before advanced score editing.
- Do not introduce paid services, cloud dependencies, or heavy ML packages without explicit EM and PM approval.

Engineering expectations:

- Keep changes scoped to the current sprint or milestone.
- Product behavior comes from Maestro and sprint cards.
- Architecture and technical constraints come from Ada.
- Backend and frontend implementation agents add or update unit tests for changed code.
- QA reviews developer tests and adds broader regression coverage where practical.
- Implementation and QA must be separate agent passes: developers move cards from `In Progress` to `QA`, Grace leaves a QA handoff, and Linus handles release review only after QA evidence exists.
- Release validation must not substitute for missing developer tests or QA review.
- Release rollback is never autonomous; Linus documents failures and suggests rollback for user/EM approval.

Default validation commands:

```powershell
npm run desktop:build
npm run desktop:test
.venv\Scripts\python.exe -m pytest --rootdir=. apps\api\tests workers\ai\tests
.venv\Scripts\python.exe -m compileall apps\api workers\ai
```
