from pathlib import PureWindowsPath

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.job import CreateJobRequest, JobResponse, SourceType
from app.services.job_service import job_service

router = APIRouter()

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac"}
MAX_UPLOAD_BYTES = 100 * 1024 * 1024
UPLOAD_READ_CHUNK_BYTES = 1024 * 1024


@router.post("", response_model=JobResponse, status_code=201)
def create_job(payload: CreateJobRequest) -> JobResponse:
    return job_service.create_job(payload)


@router.post("/upload", response_model=JobResponse, status_code=201)
async def upload_audio_job(file: UploadFile = File(...)) -> JobResponse:
    source_name = _source_name_from_upload(file)
    _validate_upload_extension(source_name)
    await _validate_upload_size(file)

    return job_service.create_job(
        CreateJobRequest(source_type=SourceType.UPLOAD, source_name=source_name)
    )


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


def _source_name_from_upload(file: UploadFile) -> str:
    source_name = PureWindowsPath(file.filename or "").name
    if not source_name:
        raise HTTPException(
            status_code=400,
            detail="Audio file needs a filename ending in WAV, MP3, or FLAC.",
        )
    return source_name


def _validate_upload_extension(source_name: str) -> None:
    extension = PureWindowsPath(source_name).suffix.lower()
    if extension not in SUPPORTED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format. Use a WAV, MP3, or FLAC file.",
        )


async def _validate_upload_size(file: UploadFile) -> None:
    bytes_read = 0

    while chunk := await file.read(UPLOAD_READ_CHUNK_BYTES):
        bytes_read += len(chunk)
        if bytes_read > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail="Audio file is too large. Upload a file up to 100 MB.",
            )

    if bytes_read == 0:
        raise HTTPException(
            status_code=400,
            detail="Audio file is empty. Choose a WAV, MP3, or FLAC file.",
        )
