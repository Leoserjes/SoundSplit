from app.models.job import Artifact, ArtifactKind, CreateJobRequest, JobResponse, JobStatus


class JobService:
    def __init__(self) -> None:
        self._jobs: dict[str, JobResponse] = {}

    def create_job(self, payload: CreateJobRequest) -> JobResponse:
        job = JobResponse(
            status=JobStatus.QUEUED,
            source_type=payload.source_type,
            source_name=payload.source_name,
            artifacts=[
                Artifact(kind=ArtifactKind.STEM, name="Vocals"),
                Artifact(kind=ArtifactKind.STEM, name="Drums"),
                Artifact(kind=ArtifactKind.STEM, name="Bass"),
                Artifact(kind=ArtifactKind.MIDI, name="Lead melody MIDI"),
                Artifact(kind=ArtifactKind.MUSICXML, name="Lead melody MusicXML"),
            ],
        )
        self._jobs[job.id] = job
        return job

    def get_job(self, job_id: str) -> JobResponse | None:
        return self._jobs.get(job_id)


job_service = JobService()

