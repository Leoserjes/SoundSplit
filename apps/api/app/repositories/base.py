from abc import ABC, abstractmethod
from typing import Optional

from app.models.job import JobResponse


class JobRepository(ABC):
    @abstractmethod
    def create_job(self, job: JobResponse) -> JobResponse:
        """Persist a new job."""
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Optional[JobResponse]:
        """Retrieve a job by its unique identifier."""
        pass

    @abstractmethod
    def update_job(self, job: JobResponse) -> JobResponse:
        """Update an existing job record."""
        pass

    @abstractmethod
    def list_jobs(self, limit: int = 50) -> list[JobResponse]:
        """List recent jobs."""
        pass
