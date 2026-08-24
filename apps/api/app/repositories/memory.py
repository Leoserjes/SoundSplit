from typing import Optional

from app.models.job import JobResponse
from app.repositories.base import JobRepository


class InMemoryJobRepository(JobRepository):
    def __init__(self) -> None:
        self._jobs: dict[str, JobResponse] = {}

    def create_job(self, job: JobResponse) -> JobResponse:
        self._jobs[job.id] = job
        return job

    def get_job(self, job_id: str) -> Optional[JobResponse]:
        return self._jobs.get(job_id)

    def update_job(self, job: JobResponse) -> JobResponse:
        self._jobs[job.id] = job
        return job

    def list_jobs(self, limit: int = 50) -> list[JobResponse]:
        return list(self._jobs.values())[:limit]
