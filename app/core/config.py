"""Application configuration management."""

import json
from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Project
    PROJECT_NAME: str = "FastAPI Production Boilerplate"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A production-grade FastAPI boilerplate"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Admin User (created on startup)
    ADMIN_EMAIL: Optional[str] = None
    ADMIN_USERNAME: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None
    ADMIN_FULL_NAME: str = "Site Administrator"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_HOSTS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS", "ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_list(cls, v):
        """Parse JSON string or return list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [item.strip() for item in v.split(",")]
        return v

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Redis (optional)
    REDIS_URL: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
