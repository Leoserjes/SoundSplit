# harmonIA MVP Roadmap

## Milestone 1: Project Skeleton

- Repository structure
- Desktop app shell
- FastAPI app shell
- AI worker shell
- Shared job/status contracts
- Local infrastructure config

## Milestone 2: Local API Flow

- Health endpoint
- Create analysis job
- Get job status
- Store job metadata in memory first
- Return mocked analysis results

## Milestone 3: Desktop Flow

- Project screen
- Audio drag-and-drop
- Submit file to API
- Show job progress
- Display mocked results

## Milestone 4: First Real Audio Pipeline

- Accept local audio file
- Normalize audio
- Run stem separation with an existing model
- Save stems
- Return downloadable artifact metadata

## Milestone 5: First Transcription Output

- Generate MIDI for one target part
- Export MusicXML
- Export PDF if notation tooling is available
- Display artifacts in desktop app

## Planned Sprint Mapping

- Sprint 03 / `v0.4.0`: Connected desktop distribution readiness.
- Sprint 04 / `v0.5.0`: Durable jobs and artifacts.
- Sprint 05 / `v0.6.0`: Worker pipeline and audio normalization.
- Sprint 06 / `v0.7.0`: First stem separation output.
- Sprint 07 / `v0.8.0`: First MIDI transcription output.
- Sprint 08 / `v0.9.0`: MusicXML and internal alpha readiness.

Detailed planning and active sprint cards are tracked in **GitHub Projects**.

## Later

- YouTube/Spotify ingestion after legal and technical review
- User accounts and licensing
- Advanced instrument detection
- Score editor
- DAW integration
- Local/offline model mode
