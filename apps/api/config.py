"""
Configuration settings for REORCH API.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "reorch"
    postgres_password: str = "changeme"
    postgres_db: str = "reorch"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_queue: str = "reorch:jobs"
    
    # S3
    s3_endpoint: str = "http://localhost:9000"
    s3_public_endpoint: str = "http://localhost:9000"  # Browser-accessible endpoint for presigned URLs
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "reorch-uploads"
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def async_database_url(self) -> str:
        """Construct async PostgreSQL connection URL for asyncpg."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
