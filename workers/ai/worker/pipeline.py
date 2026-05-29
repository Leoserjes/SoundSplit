from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineResult:
    job_id: str
    artifacts: list[str]


class AudioPipeline:
    def run(self, job_id: str) -> PipelineResult:
        artifacts = [
            "vocals.wav",
            "drums.wav",
            "bass.wav",
            "lead_melody.mid",
            "lead_melody.musicxml",
        ]
        return PipelineResult(job_id=job_id, artifacts=artifacts)

