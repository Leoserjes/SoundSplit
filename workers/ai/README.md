# SoundSplit AI Worker

Python worker for long-running harmonIA audio processing.

Initial responsibilities:

- Receive queued analysis jobs
- Normalize audio
- Run stem separation
- Run transcription
- Generate MIDI, MusicXML, and PDF score artifacts
- Report progress and artifact metadata back to the API

The first implementation can use mocked output, then add real models incrementally.

