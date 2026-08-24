import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from app.core.config import settings


class StorageService(ABC):
    @abstractmethod
    def save_upload(self, job_id: str, filename: str, content: bytes) -> Path:
        """Store uploaded audio file bytes for a given job."""
        pass

    @abstractmethod
    def get_upload_path(self, job_id: str) -> Optional[Path]:
        """Get the filesystem path for an uploaded audio file."""
        pass

    @abstractmethod
    def save_artifact(self, job_id: str, artifact_name: str, content: bytes) -> Path:
        """Store a generated or placeholder artifact for a job."""
        pass

    @abstractmethod
    def get_artifact_path(self, job_id: str, artifact_name: str) -> Optional[Path]:
        """Get the filesystem path for a generated artifact."""
        pass

    @abstractmethod
    def delete_job_files(self, job_id: str) -> bool:
        """Delete all storage files associated with a job."""
        pass


class LocalStorageService(StorageService):
    def __init__(self, root_dir: str = "data") -> None:
        self.root_dir = Path(root_dir)
        self.uploads_dir = self.root_dir / "uploads"
        self.artifacts_dir = self.root_dir / "artifacts"
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        # Protect against path traversal
        clean = Path(filename).name
        clean = re.sub(r"[^\w\.-]", "_", clean)
        return clean or "audio_file"

    def save_upload(self, job_id: str, filename: str, content: bytes) -> Path:
        job_dir = self.uploads_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        safe_filename = self._sanitize_filename(filename)
        dest = job_dir / safe_filename
        dest.write_bytes(content)
        return dest

    def get_upload_path(self, job_id: str) -> Optional[Path]:
        job_dir = self.uploads_dir / job_id
        if not job_dir.exists():
            return None
        files = list(job_dir.glob("*"))
        return files[0] if files else None

    def save_artifact(self, job_id: str, artifact_name: str, content: bytes) -> Path:
        job_dir = self.artifacts_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        safe_name = self._sanitize_filename(artifact_name)
        dest = job_dir / safe_name
        dest.write_bytes(content)
        return dest

    def get_artifact_path(self, job_id: str, artifact_name: str) -> Optional[Path]:
        safe_name = self._sanitize_filename(artifact_name)
        dest = self.artifacts_dir / job_id / safe_name
        return dest if dest.exists() else None

    def delete_job_files(self, job_id: str) -> bool:
        deleted = False
        for parent in (self.uploads_dir, self.artifacts_dir):
            target = parent / job_id
            if target.exists():
                for f in target.iterdir():
                    f.unlink(missing_ok=True)
                target.rmdir()
                deleted = True
        return deleted


storage_service = LocalStorageService(root_dir=settings.storage_root)
