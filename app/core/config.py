from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.system import get_optimal_workers


class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = Field(default="SIPS")
    VERSION: str = Field(default="0.1.0")
    DESCRIPTION: str = Field(default="SIPS API")

    # Server settings
    DEBUG: bool = Field(default=False)
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    WORKERS: int = Field(default=get_optimal_workers())
    LOG_LEVEL: str = Field(default="info")
    LOOP: str = Field(default="uvloop")
    HTTP: str = Field(default="httptools")
    LIMIT_CONCURRENCY: int = Field(default=100)
    BACKLOG: int = Field(default=2048)
    LIMIT_MAX_REQUESTS: int | None = Field(default=None)
    TIMEOUT_KEEP_ALIVE: int = Field(default=5)
    H11_MAX_INCOMPLETE_EVENT_SIZE: int = Field(default=16 * 1024)
    SERVER_HEADER: str = Field(default=f"{PROJECT_NAME}/{VERSION}")
    FORWARDED_ALLOW_IPS: str = Field(default="*")
    DATE_HEADER: bool = Field(default=True)

    @property
    def ACCESS_LOG(self) -> bool:
        return self.DEBUG

    # Database settings
    DATABASE_URL: str

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # Cors settings
    ALLOWED_ORIGINS: List[str] = Field(default=["*"])

    # S3/MinIO settings
    MINIO_ENDPOINT_URL: str = Field(default="http://localhost:9000")
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_SECURE: Optional[bool] = False
    MINIO_BUCKET_NAME: Optional[str] = Field(default="sips")
    MINIO_REGION: Optional[str] = Field(default=None)

    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB default limit
    ALLOWED_EXTENSIONS: List[str] = [
        "jpg",
        "jpeg",
        "png",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "txt",
        "csv",
        "zip",
        "rar",
        "json",
    ]

    TIMEZONE: str = Field(default="Asia/Jakarta")

    # Settings config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="allow")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
