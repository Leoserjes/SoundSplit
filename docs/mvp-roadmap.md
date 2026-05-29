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

## Later

- YouTube/Spotify ingestion after legal and technical review
- User accounts and licensing
- Advanced instrument detection
- Score editor
- DAW integration
- Local/offline model mode

