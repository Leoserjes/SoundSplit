from pathlib import PureWindowsPath

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.job import CreateJobRequest, JobResponse, SourceType
from app.services.job_service import job_service
from app.services.storage_service import storage_service

router = APIRouter()

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac"}
MAX_UPLOAD_BYTES = 100 * 1024 * 1024
UPLOAD_READ_CHUNK_BYTES = 1024 * 1024


@router.post(
    "",
    response_model=JobResponse,
    status_code=201,
    summary="Create analysis job",
    description="Create a new music analysis job from audio metadata.",
    responses={
        201: {"description": "Analysis job created successfully."},
        422: {"description": "Validation error in request payload."},
    },
)
def create_job(payload: CreateJobRequest) -> JobResponse:
    return job_service.create_job(payload)


@router.post(
    "/upload",
    response_model=JobResponse,
    status_code=201,
    summary="Upload audio and create analysis job",
    description="Upload a local WAV, MP3, or FLAC audio file (up to 100 MB) and create an analysis job.",
    responses={
        201: {"description": "Audio uploaded and job queued successfully."},
        400: {"description": "Invalid format or empty file."},
        413: {"description": "File exceeds maximum size of 100 MB."},
    },
)
async def upload_audio_job(file: UploadFile = File(..., description="Audio file (.wav, .mp3, .flac)")) -> JobResponse:
    source_name = _source_name_from_upload(file)
    _validate_upload_extension(source_name)
    file_bytes = await _read_and_validate_upload(file)

    job = job_service.create_job(
        CreateJobRequest(source_type=SourceType.UPLOAD, source_name=source_name)
    )

    storage_service.save_upload(job.id, source_name, file_bytes)
    return job


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get analysis job status",
    description="Retrieve status, metadata, and artifact summary for an existing analysis job.",
    responses={
        200: {"description": "Job details found."},
        404: {"description": "Job not found."},
    },
)
def get_job(job_id: str) -> JobResponse:
    job = job_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.get(
    "/{job_id}/artifacts",
    summary="List job artifacts",
    description="List all generated and placeholder artifacts (stems, MIDI, MusicXML) for an analysis job.",
    responses={
        200: {"description": "List of artifacts for the job."},
        404: {"description": "Job not found."},
    },
)
def get_job_artifacts(job_id: str) -> dict[str, list[dict[str, str | None]]]:
    job = job_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"artifacts": [artifact.model_dump() for artifact in job.artifacts]}


from fastapi.responses import FileResponse, Response


@router.get(
    "/{job_id}/artifacts/{artifact_id}/download",
    summary="Download job artifact",
    description="Download the generated audio stem, MIDI, or MusicXML score file for an artifact.",
    responses={
        200: {"description": "Artifact file stream."},
        404: {"description": "Job or artifact file not found."},
    },
)
def download_job_artifact(job_id: str, artifact_id: str) -> Response:
    job = job_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    target_artifact = next(
        (art for art in job.artifacts if art.id == artifact_id or art.name == artifact_id),
        None,
    )
    if target_artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found")

    file_path = storage_service.get_artifact_path(job_id, artifact_id)
    if file_path is None or not file_path.exists():
        # Fallback to name search
        file_path = storage_service.get_artifact_path(job_id, target_artifact.name)

    if file_path is None or not file_path.exists():
        raise HTTPException(status_code=404, detail="Artifact file not found in storage")

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream",
    )


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


async def _read_and_validate_upload(file: UploadFile) -> bytes:
    chunks = []
    bytes_read = 0

    while chunk := await file.read(UPLOAD_READ_CHUNK_BYTES):
        chunks.append(chunk)
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

    return b"".join(chunks)
