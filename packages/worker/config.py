"""
Configuration settings for REORCH Worker.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Worker settings loaded from environment variables."""

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_queue: str = "reorch:jobs"

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "reorch"
    postgres_password: str = "changeme"
    postgres_db: str = "reorch"

    # S3
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "reorch-uploads"

    # Worker
    worker_concurrency: int = 2
    job_timeout: int = 300  # 5 minutes

    # Audio pipeline
    target_lufs: float = -14.0
    temp_dir: str = "/tmp/reorch"

    # Demucs stem separation
    demucs_model: str = "htdemucs"
    demucs_device: str = "auto"  # "auto", "cpu", or "cuda"
    demucs_shifts: int = 1  # Higher = better quality but slower

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
