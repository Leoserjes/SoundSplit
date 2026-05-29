from datetime import datetime, timezone
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    CREATED = "created"
    UPLOADING = "uploading"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SourceType(StrEnum):
    UPLOAD = "upload"
    YOUTUBE = "youtube"
    SPOTIFY = "spotify"


class ArtifactKind(StrEnum):
    STEM = "stem"
    MIDI = "midi"
    MUSICXML = "musicxml"
    PDF = "pdf"
    LOG = "log"


class ArtifactStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"


class Artifact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    kind: ArtifactKind
    name: str
    status: ArtifactStatus = ArtifactStatus.PENDING
    uri: str | None = None


class CreateJobRequest(BaseModel):
    source_type: SourceType = SourceType.UPLOAD
    source_name: str | None = None


class JobResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    status: JobStatus = JobStatus.CREATED
    source_type: SourceType
    source_name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: str | None = None
    artifacts: list[Artifact] = Field(default_factory=list)

