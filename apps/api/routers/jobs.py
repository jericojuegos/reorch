"""
Jobs API router.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Job, JobStatus, Track


router = APIRouter()


# === Schemas ===

class JobCreate(BaseModel):
    """Schema for creating a job."""
    track_id: str
    preset: str = "ballad_to_rock"


class JobResponse(BaseModel):
    """Schema for job response."""
    id: str
    track_id: str
    preset: str
    status: str
    progress: int
    error_message: Optional[str]
    output_path: Optional[str]
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]

    class Config:
        from_attributes = True


# === Endpoints ===

@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new re-orchestration job."""
    # Verify track exists
    result = await db.execute(select(Track).where(Track.id == job.track_id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    db_job = Job(
        track_id=job.track_id,
        preset=job.preset,
        status=JobStatus.QUEUED,
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)

    # TODO: Enqueue to Redis here

    return JobResponse(
        id=db_job.id,
        track_id=db_job.track_id,
        preset=db_job.preset,
        status=db_job.status.value,
        progress=db_job.progress,
        error_message=db_job.error_message,
        output_path=db_job.output_path,
        created_at=db_job.created_at.isoformat(),
        started_at=db_job.started_at.isoformat() if db_job.started_at else None,
        completed_at=db_job.completed_at.isoformat() if db_job.completed_at else None,
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a job by ID."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(
        id=job.id,
        track_id=job.track_id,
        preset=job.preset,
        status=job.status.value,
        progress=job.progress,
        error_message=job.error_message,
        output_path=job.output_path,
        created_at=job.created_at.isoformat(),
        started_at=job.started_at.isoformat() if job.started_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
    )


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List jobs, optionally filtered by status."""
    query = select(Job).order_by(Job.created_at.desc())
    if status:
        query = query.where(Job.status == JobStatus(status))
    result = await db.execute(query)
    jobs = result.scalars().all()
    return [
        JobResponse(
            id=j.id,
            track_id=j.track_id,
            preset=j.preset,
            status=j.status.value,
            progress=j.progress,
            error_message=j.error_message,
            output_path=j.output_path,
            created_at=j.created_at.isoformat(),
            started_at=j.started_at.isoformat() if j.started_at else None,
            completed_at=j.completed_at.isoformat() if j.completed_at else None,
        )
        for j in jobs
    ]
