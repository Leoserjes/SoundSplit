# SoundSplit AI Worker

The current `AudioPipeline` is a stub that returns artifact names. It does not consume queued jobs, process audio, persist output files, or update API job status. API placeholder files are currently created by `JobService`.

Real normalization, separation, and transcription are future work tracked in GitHub Projects. See the [architecture](../../docs/architecture.md) and root [setup](../../README.md#getting-started). Local embedding service instructions are in [knowledge retrieval](../../docs/knowledge-retrieval.md).
