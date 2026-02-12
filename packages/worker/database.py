"""
Database access for the REORCH Worker.
"""
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# Valid job status values (whitelist for safe interpolation)
VALID_STATUSES = {"queued", "running", "succeeded", "failed"}

# Build async database URL
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def update_job_status(
    job_id: str,
    status: str,
    progress: int | None = None,
    error_message: str | None = None,
    output_path: str | None = None,
) -> None:
    """Update job status and optional fields in the database."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    async with AsyncSessionLocal() as session:
        # Status uses safe interpolation (whitelisted above) because
        # asyncpg cannot bind text parameters to PostgreSQL custom enums.
        set_parts = [f"status = '{status}'"]
        params: dict = {"job_id": job_id}

        if progress is not None:
            set_parts.append("progress = :progress")
            params["progress"] = progress
        if error_message is not None:
            set_parts.append("error_message = :error_message")
            params["error_message"] = error_message
        if output_path is not None:
            set_parts.append("output_path = :output_path")
            params["output_path"] = output_path

        if status == "running":
            set_parts.append("started_at = :ts")
            params["ts"] = datetime.utcnow()
        elif status in ("succeeded", "failed"):
            set_parts.append("completed_at = :ts")
            params["ts"] = datetime.utcnow()

        sql = f"UPDATE jobs SET {', '.join(set_parts)} WHERE id = :job_id"
        await session.execute(text(sql), params)
        await session.commit()


async def update_job_progress(job_id: str, progress: int) -> None:
    """Update job progress percentage."""
    async with AsyncSessionLocal() as session:
        await session.execute(
            text("UPDATE jobs SET progress = :progress WHERE id = :job_id"),
            {"progress": progress, "job_id": job_id},
        )
        await session.commit()
