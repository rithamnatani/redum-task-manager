from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "please-change-me"

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
