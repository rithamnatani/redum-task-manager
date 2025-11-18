from typing import Any

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "please-change-me"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:4200",
        "http://localhost:8080",
    ]
    CHROMA_DB_PATH: str = "./chroma-storage"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "models/gemini-1.5-flash"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: Any) -> list[str]:  # noqa: N805
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return value
        raise ValueError("Invalid BACKEND_CORS_ORIGINS format")

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
