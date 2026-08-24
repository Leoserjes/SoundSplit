import pytest
from fastapi.testclient import TestClient

from app.api.routes import jobs as jobs_routes
from app.main import app


client = TestClient(app)
CREATE_JOB_PAYLOAD = {"source_type": "upload", "source_name": "demo.wav"}


def create_job() -> dict[str, object]:
    response = client.post("/v1/jobs", json=CREATE_JOB_PAYLOAD)

    assert response.status_code == 201
    return response.json()


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "soundsplit-api"}


def test_create_analysis_job() -> None:
    job = create_job()

    assert isinstance(job["id"], str)
    assert job["status"] == "queued"
    assert job["source_type"] == "upload"
    assert job["source_name"] == "demo.wav"
    assert isinstance(job["created_at"], str)
    assert isinstance(job["updated_at"], str)
    assert job["error"] is None
    assert len(job["artifacts"]) == 5
    assert all(
        set(artifact) == {"id", "kind", "name", "status", "uri"}
        for artifact in job["artifacts"]
    )


@pytest.mark.parametrize("filename", ["song.wav", "song.mp3", "song.flac"])
def test_upload_audio_file_creates_analysis_job(filename: str) -> None:
    response = client.post(
        "/v1/jobs/upload",
        files={"file": (filename, b"audio-bytes", "application/octet-stream")},
    )

    assert response.status_code == 201

    job = response.json()
    assert isinstance(job["id"], str)
    assert job["status"] == "queued"
    assert job["source_type"] == "upload"
    assert job["source_name"] == filename
    assert job["error"] is None
    assert len(job["artifacts"]) == 5


def test_upload_audio_file_rejects_unsupported_extension() -> None:
    response = client.post(
        "/v1/jobs/upload",
        files={"file": ("notes.txt", b"audio-bytes", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unsupported audio format. Use a WAV, MP3, or FLAC file."
    }


def test_upload_audio_file_rejects_empty_file() -> None:
    response = client.post(
        "/v1/jobs/upload",
        files={"file": ("empty.wav", b"", "audio/wav")},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Audio file is empty. Choose a WAV, MP3, or FLAC file."
    }


def test_upload_audio_file_rejects_oversized_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(jobs_routes, "MAX_UPLOAD_BYTES", 8)

    response = client.post(
        "/v1/jobs/upload",
        files={"file": ("large.wav", b"too-large", "audio/wav")},
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "Audio file is too large. Upload a file up to 100 MB."
    }


def test_fetch_analysis_job() -> None:
    job = create_job()

    response = client.get(f"/v1/jobs/{job['id']}")

    assert response.status_code == 200
    assert response.json() == job


def test_fetch_analysis_job_artifacts() -> None:
    job = create_job()

    response = client.get(f"/v1/jobs/{job['id']}/artifacts")

    assert response.status_code == 200
    assert response.json() == {"artifacts": job["artifacts"]}


@pytest.mark.parametrize(
    "path",
    [
        "/v1/jobs/missing-job-id",
        "/v1/jobs/missing-job-id/artifacts",
    ],
)
def test_missing_analysis_job_returns_404(path: str) -> None:
    response = client.get(path)

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}


@pytest.mark.parametrize(
    "origin",
    [
        "http://localhost:1420",
        "http://127.0.0.1:1420",
    ],
)
@pytest.mark.parametrize("path", ["/v1/jobs", "/v1/jobs/upload"])
def test_analysis_job_cors_preflight(origin: str, path: str) -> None:
    response = client.options(
        path,
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"].lower()

    if path == "/v1/jobs":
        create_response = client.post(path, json=CREATE_JOB_PAYLOAD, headers={"Origin": origin})
    else:
        create_response = client.post(
            path,
            files={"file": ("song.wav", b"audio-bytes", "audio/wav")},
            headers={"Origin": origin},
        )

    assert create_response.status_code == 201
    assert create_response.headers["access-control-allow-origin"] == origin


def test_create_analysis_job_cors_rejects_unlisted_origin() -> None:
    response = client.options(
        "/v1/jobs",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_openapi_schema_endpoint() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()

    assert schema["info"]["title"] == "SoundSplit API"
    assert schema["info"]["version"] == "0.5.0"
    paths = schema["paths"]

    assert "/health" in paths
    assert "get" in paths["/health"]

    assert "/v1/jobs" in paths
    assert "post" in paths["/v1/jobs"]

    assert "/v1/jobs/upload" in paths
    assert "post" in paths["/v1/jobs/upload"]

    assert "/v1/jobs/{job_id}" in paths
    assert "get" in paths["/v1/jobs/{job_id}"]

    assert "/v1/jobs/{job_id}/artifacts" in paths
    assert "get" in paths["/v1/jobs/{job_id}/artifacts"]

    assert "/v1/jobs/{job_id}/artifacts/{artifact_id}/download" in paths
    assert "get" in paths["/v1/jobs/{job_id}/artifacts/{artifact_id}/download"]


def test_sqlite_repository_persistence(tmp_path: pytest.TempPathFactory) -> None:
    from app.models.job import CreateJobRequest, SourceType
    from app.repositories.sqlite import SQLiteJobRepository
    from app.services.job_service import JobService

    db_path = str(tmp_path / "test_soundsplit.db")
    repo1 = SQLiteJobRepository(db_path=db_path)
    service1 = JobService(repository=repo1)

    created_job = service1.create_job(
        CreateJobRequest(source_type=SourceType.UPLOAD, source_name="persist_test.wav")
    )
    job_id = created_job.id

    # Simulate API process restart with a fresh service instance on the same SQLite file
    repo2 = SQLiteJobRepository(db_path=db_path)
    service2 = JobService(repository=repo2)

    persisted_job = service2.get_job(job_id)
    assert persisted_job is not None
    assert persisted_job.id == job_id
    assert persisted_job.source_name == "persist_test.wav"
    assert persisted_job.status.value == "queued"
    assert len(persisted_job.artifacts) == 5


def test_upload_audio_file_persists_bytes_in_storage() -> None:
    from app.services.storage_service import storage_service

    test_content = b"RIFF-WAVE-TEST-AUDIO-BYTES"
    response = client.post(
        "/v1/jobs/upload",
        files={"file": ("persist_audio.wav", test_content, "audio/wav")},
    )

    assert response.status_code == 201
    job_id = response.json()["id"]

    upload_path = storage_service.get_upload_path(job_id)
    assert upload_path is not None
    assert upload_path.exists()
    assert upload_path.read_bytes() == test_content

    # Clean up test artifacts
    storage_service.delete_job_files(job_id)


def test_download_artifact_success() -> None:
    from app.services.storage_service import storage_service

    create_response = client.post("/v1/jobs", json=CREATE_JOB_PAYLOAD)
    assert create_response.status_code == 201
    job = create_response.json()
    job_id = job["id"]
    first_artifact = job["artifacts"][0]
    artifact_id = first_artifact["id"]

    download_response = client.get(f"/v1/jobs/{job_id}/artifacts/{artifact_id}/download")
    assert download_response.status_code == 200
    assert len(download_response.content) > 0

    # Cleanup
    storage_service.delete_job_files(job_id)


def test_download_artifact_not_found() -> None:
    response = client.get("/v1/jobs/nonexistent-job-id/artifacts/nonexistent-art/download")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"




