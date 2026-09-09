"""Settings load on construction, never on module import."""

from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = Field(default=8000, ge=1, le=65535)
    postgres_host: str = "localhost"
    postgres_port: int = Field(default=5432, ge=1, le=65535)
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    redis_host: str = "localhost"
    redis_port: int = Field(default=6379, ge=1, le=65535)
    chroma_persist_directory: Path = Path("./chroma_data")
    openai_api_key: SecretStr = SecretStr("")

    @field_validator("chroma_persist_directory", mode="after")
    @classmethod
    def resolve_chroma_path(cls, value: Path) -> Path:
        return (PROJECT_ROOT / value).resolve()
