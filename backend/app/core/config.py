"""Settings load on construction, never on module import."""

from pathlib import Path
from typing import Literal

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
    candidate_data_mode: Literal["mock", "snapshot"] = "mock"
    candidate_snapshot_path: Path | None = None
    openai_api_key: SecretStr = SecretStr("")
    openai_model: str = ""
    openai_max_output_tokens: int = Field(default=1024, ge=256, le=2000)
    openai_reasoning_effort: Literal["low"] = "low"
    agent_planner: Literal["deterministic", "openai"] = "deterministic"
    semantic_augmentation_mode: Literal["deterministic", "hybrid"] = "deterministic"
    semantic_extractor_prompt_version: Literal[
        "semantic_extractor_v1", "semantic_extractor_v2", "semantic_extractor_v3"
    ] = "semantic_extractor_v3"
    planner_prompt_version: Literal["planner_v1"] = "planner_v1"

    @field_validator("chroma_persist_directory", mode="after")
    @classmethod
    def resolve_chroma_path(cls, value: Path) -> Path:
        return (PROJECT_ROOT / value).resolve()

    @field_validator("candidate_snapshot_path", mode="after")
    @classmethod
    def resolve_candidate_snapshot_path(cls, value: Path | None) -> Path | None:
        return (PROJECT_ROOT / value).resolve() if value is not None else None
