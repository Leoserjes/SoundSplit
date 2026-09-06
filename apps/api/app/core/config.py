from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = Field(default="development", alias="SOUNDSPLIT_ENV")
    database_url: str = "postgresql+psycopg://soundsplit:soundsplit@localhost:5432/soundsplit"
    sqlite_db_path: str = "data/soundsplit.db"
    storage_root: str = "data"
    redis_url: str = "redis://localhost:6379/0"
    s3_endpoint_url: str = "http://localhost:9000"
    s3_bucket: str = "soundsplit-local"
    knowledge_database_url: str = Field(
        default="postgresql://soundsplit:soundsplit@localhost:5432/soundsplit",
        alias="KNOWLEDGE_DATABASE_URL",
    )
    notion_knowledge_root_id: str = Field(
        default="3d381a9a-01d0-811a-beb0-d6bcd51cc668",
        alias="NOTION_KNOWLEDGE_ROOT_ID",
    )
    knowledge_embedding_url: str = Field(
        default="http://127.0.0.1:8091", alias="KNOWLEDGE_EMBEDDING_URL"
    )
    knowledge_max_age_hours: int = Field(default=24, ge=1, le=168)
    knowledge_min_similarity: float = Field(default=0.45, ge=-1, le=1)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
