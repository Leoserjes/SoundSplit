import pytest
from fastapi.testclient import TestClient

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
def test_create_analysis_job_cors_preflight(origin: str) -> None:
    response = client.options(
        "/v1/jobs",
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

    create_response = client.post("/v1/jobs", json=CREATE_JOB_PAYLOAD, headers={"Origin": origin})

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
