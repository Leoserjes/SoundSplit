from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = Field(default="development", alias="SOUNDSPLIT_ENV")
    database_url: str = "postgresql+psycopg://soundsplit:soundsplit@localhost:5432/soundsplit"
    redis_url: str = "redis://localhost:6379/0"
    s3_endpoint_url: str = "http://localhost:9000"
    s3_bucket: str = "soundsplit-local"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
