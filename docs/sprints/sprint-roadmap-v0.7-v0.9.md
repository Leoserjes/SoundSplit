# Future Sprint Roadmap: v0.7.0 To v0.9.0

Status: Directional draft

This roadmap keeps the post-worker plan visible without overcommitting before Sprint 04 and Sprint 05 reveal persistence, storage, worker, audio tooling, and packaging constraints.

## Sprint 06: v0.7.0 First Stem Separation Output

Planned window: 2026-08-02 to 2026-08-16

Goal:

Introduce the first proven stem-separation path and produce downloadable stem artifacts through the durable artifact pipeline.

Candidate cards:

- Decide stem separation model and runtime.
- Review model license, package size, CPU/GPU expectations, and Windows impact.
- Add a model runner abstraction.
- Generate first stem artifacts for supported inputs.
- Store stems through the Sprint 04 artifact boundary.
- Update desktop artifact grouping for stems.
- Document performance limits and timeouts.
- QA review and release `v0.7.0`.

Required gate:

- EM and PM must approve any heavy ML package, model download, or runtime dependency before implementation.

Out of scope:

- MIDI transcription.
- MusicXML/PDF export.
- Offline model packaging for public distribution.
- Paid cloud processing.

## Sprint 07: v0.8.0 First MIDI Transcription Output

Planned window: 2026-08-17 to 2026-08-31

Goal:

Generate the first editable MIDI artifact from one target part or stem, with clear quality limitations.

Candidate cards:

- Choose the first target part for transcription.
- Decide transcription approach and dependency footprint.
- Generate one MIDI artifact from the approved target input.
- Add or update MIDI artifact contract coverage.
- Add desktop download/display behavior for MIDI.
- Document transcription quality limits and expected failures.
- QA review and release `v0.8.0`.

Required gate:

- Product must approve the first target part and user promise before implementation.

Out of scope:

- Full arrangement transcription.
- Advanced instrument detection.
- Score editor.
- DAW integration.

## Sprint 08: v0.9.0 MusicXML And Internal Alpha Readiness

Planned window: 2026-09-01 to 2026-09-15

Goal:

Convert the first MIDI output into notation-oriented artifacts and prepare a safer internal alpha validation loop.

Candidate cards:

- Generate MusicXML from the approved MIDI path.
- Evaluate PDF export feasibility and decide whether it belongs in alpha.
- Improve desktop artifact organization for source, normalized audio, stems, MIDI, and notation.
- Define artifact retention and cleanup rules.
- Create internal alpha checklist: install, upload, process, download, and review safety.
- Review stored uploaded audio and artifact privacy implications.
- QA review and release `v0.9.0`.

Required gate:

- QA and Release must confirm internal alpha safety boundaries before inviting non-developer testers.

Out of scope:

- Public launch.
- User accounts and licensing.
- YouTube or Spotify ingestion.
- Advanced score editing.

## Cross-Sprint Dependencies

- Sprint 06 depends on Sprint 05 worker execution and Sprint 04 artifact storage.
- Sprint 07 depends on a stable source audio or stem artifact from Sprint 06.
- Sprint 08 depends on a stable MIDI artifact from Sprint 07.
- Distribution and installer work from Sprint 03 remains a safety gate for internal testers, but it does not replace product validation.

## Watch Items

- Heavy ML packages can affect installer size, CI time, and local machine requirements.
- Audio libraries may require system dependencies that are harder to package on Windows.
- Stored uploaded audio creates retention, privacy, and cleanup responsibilities.
- Quality expectations must remain modest until the first real pipeline is tested with varied audio.
- Paid services, certificates, or cloud processing require explicit EM and PM approval.
