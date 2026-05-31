from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.jobs import router as jobs_router

DEVELOPMENT_CORS_ORIGINS = [
    "http://localhost:1420",
    "http://127.0.0.1:1420",
]

app = FastAPI(
    title="SoundSplit API",
    version="0.2.0",
    description="Backend orchestration API for harmonIA.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEVELOPMENT_CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "soundsplit-api"}


app.include_router(jobs_router, prefix="/v1/jobs", tags=["jobs"])
