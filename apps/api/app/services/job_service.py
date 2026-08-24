from typing import Optional

from app.core.config import settings
from app.models.job import Artifact, ArtifactKind, CreateJobRequest, JobResponse, JobStatus
from app.repositories import InMemoryJobRepository, JobRepository, SQLiteJobRepository


class JobService:
    def __init__(self, repository: Optional[JobRepository] = None) -> None:
        if repository is not None:
            self._repository = repository
        elif settings.environment == "test":
            self._repository = InMemoryJobRepository()
        else:
            self._repository = SQLiteJobRepository(db_path=settings.sqlite_db_path)

    def create_job(self, payload: CreateJobRequest) -> JobResponse:
        from uuid import uuid4
        from app.models.job import ArtifactStatus
        from app.services.storage_service import storage_service

        artifacts_def = [
            (ArtifactKind.STEM, "Vocals", "vocals.wav", b"RIFF-WAVE-VOCALS-SAMPLE-DATA"),
            (ArtifactKind.STEM, "Drums", "drums.wav", b"RIFF-WAVE-DRUMS-SAMPLE-DATA"),
            (ArtifactKind.STEM, "Bass", "bass.wav", b"RIFF-WAVE-BASS-SAMPLE-DATA"),
            (ArtifactKind.MIDI, "Lead melody MIDI", "lead_melody.mid", b"MThd-MIDI-SAMPLE-DATA"),
            (ArtifactKind.MUSICXML, "Lead melody MusicXML", "lead_melody.musicxml", b"<?xml version='1.0'?><score-partwise/>"),
        ]

        from uuid import uuid4
        job_id = str(uuid4())

        artifacts = []
        for kind, name, filename, sample_bytes in artifacts_def:
            art_id = str(uuid4())
            artifacts.append(
                Artifact(
                    id=art_id,
                    kind=kind,
                    name=name,
                    status=ArtifactStatus.READY,
                    uri=f"/v1/jobs/{job_id}/artifacts/{art_id}/download",
                )
            )
            storage_service.save_artifact(job_id, filename, sample_bytes)
            storage_service.save_artifact(job_id, art_id, sample_bytes)

        job = JobResponse(
            id=job_id,
            status=JobStatus.QUEUED,
            source_type=payload.source_type,
            source_name=payload.source_name,
            artifacts=artifacts,
        )
        return self._repository.create_job(job)

    def get_job(self, job_id: str) -> Optional[JobResponse]:
        return self._repository.get_job(job_id)

    def update_job(self, job: JobResponse) -> JobResponse:
        return self._repository.update_job(job)

    def list_jobs(self, limit: int = 50) -> list[JobResponse]:
        return self._repository.list_jobs(limit=limit)


job_service = JobService()
