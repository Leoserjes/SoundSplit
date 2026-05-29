from fastapi import APIRouter, HTTPException

from app.models.job import CreateJobRequest, JobResponse
from app.services.job_service import job_service

router = APIRouter()


@router.post("", response_model=JobResponse, status_code=201)
def create_job(payload: CreateJobRequest) -> JobResponse:
    return job_service.create_job(payload)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str) -> JobResponse:
    job = job_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.get("/{job_id}/artifacts")
def get_job_artifacts(job_id: str) -> dict[str, list[dict[str, str | None]]]:
    job = job_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"artifacts": [artifact.model_dump() for artifact in job.artifacts]}

