from fastapi import FastAPI

from app.api.routes.jobs import router as jobs_router

app = FastAPI(
    title="SoundSplit API",
    version="0.1.0",
    description="Backend orchestration API for harmonIA.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "soundsplit-api"}


app.include_router(jobs_router, prefix="/v1/jobs", tags=["jobs"])

