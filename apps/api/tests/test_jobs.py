from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "soundsplit-api"}


def test_create_and_fetch_analysis_job() -> None:
    response = client.post(
        "/v1/jobs",
        json={"source_type": "upload", "source_name": "demo.wav"},
    )

    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "queued"
    assert job["source_type"] == "upload"
    assert job["source_name"] == "demo.wav"
    assert len(job["artifacts"]) == 5

    get_response = client.get(f"/v1/jobs/{job['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == job["id"]
