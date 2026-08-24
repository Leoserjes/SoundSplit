import json
import sqlite3
from pathlib import Path
from typing import Optional

from app.models.job import JobResponse
from app.repositories.base import JobRepository


class SQLiteJobRepository(JobRepository):
    def __init__(self, db_path: str = "data/soundsplit.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_name TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    data TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def create_job(self, job: JobResponse) -> JobResponse:
        payload_json = job.model_dump_json()
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO jobs (id, status, source_type, source_name, created_at, updated_at, data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.status.value,
                    job.source_type.value,
                    job.source_name,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                    payload_json,
                ),
            )
            conn.commit()
        return job

    def get_job(self, job_id: str) -> Optional[JobResponse]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT data FROM jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            data = json.loads(row["data"])
            return JobResponse.model_validate(data)

    def update_job(self, job: JobResponse) -> JobResponse:
        return self.create_job(job)

    def list_jobs(self, limit: int = 50) -> list[JobResponse]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT data FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            )
            rows = cursor.fetchall()
            return [JobResponse.model_validate(json.loads(row["data"])) for row in rows]
