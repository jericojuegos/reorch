"""
Tracks API router.
"""
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Project, Track
from s3 import s3_client
from io import BytesIO
import mutagen


router = APIRouter()


# === Constants ===

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_DURATION_SECONDS = 600.0  # 10 minutes
ALLOWED_EXTENSIONS = {'.mp3', '.wav'}
CONTENT_TYPE_MAP = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
}


# === Schemas ===

class TrackResponse(BaseModel):
    """Schema for track response."""
    id: str
    project_id: str
    filename: str
    original_filename: str
    storage_path: str
    file_size: int
    duration_seconds: Optional[float]
    format: str
    created_at: str

    class Config:
        from_attributes = True


# === Endpoints ===

@router.post("/", response_model=TrackResponse, status_code=201)
async def upload_track(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload an audio track.
    
    Validates file type (WAV/MP3) and size (max 100MB),
    uploads to S3, and creates database record.
    """
    # Validate project exists
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_ext = '.' + file.filename.rsplit('.', 1)[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file and validate size
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024 * 1024)} MB"
        )
    
    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    
    # Calculate duration
    file_bytes_io = BytesIO(file_content)
    try:
        audio = mutagen.File(file_bytes_io)
        if audio is None or not hasattr(audio, 'info'):
            raise ValueError("Could not read audio metadata")
        duration_seconds = audio.info.length
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid or corrupted audio file: {str(e)}"
        )
        
    if duration_seconds > MAX_DURATION_SECONDS:
        raise HTTPException(
            status_code=400,
            detail=f"Track is too long. Maximum duration is {MAX_DURATION_SECONDS / 60} minutes."
        )

    # Upload to S3
    content_type = CONTENT_TYPE_MAP.get(file_ext, 'application/octet-stream')
    try:
        # file_bytes_io cursor might be at EOF after mutagen, reset it
        file_bytes_io.seek(0)
        storage_path = await s3_client.upload_file(
            file_obj=file_bytes_io,
            project_id=project_id,
            filename=file.filename,
            content_type=content_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
    
    # Create database record
    db_track = Track(
        project_id=project_id,
        filename=storage_path.split('/')[-1],  # UUID-based filename
        original_filename=file.filename,
        storage_path=storage_path,
        file_size=file_size,
        duration_seconds=duration_seconds,
        format=file_ext.lstrip('.'),
    )
    db.add(db_track)
    await db.commit()
    await db.refresh(db_track)
    
    return TrackResponse(
        id=db_track.id,
        project_id=db_track.project_id,
        filename=db_track.filename,
        original_filename=db_track.original_filename,
        storage_path=db_track.storage_path,
        file_size=db_track.file_size,
        duration_seconds=db_track.duration_seconds,
        format=db_track.format,
        created_at=db_track.created_at.isoformat(),
    )


@router.get("/{track_id}", response_model=TrackResponse)
async def get_track(
    track_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a track by ID."""
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    return TrackResponse(
        id=track.id,
        project_id=track.project_id,
        filename=track.filename,
        original_filename=track.original_filename,
        storage_path=track.storage_path,
        file_size=track.file_size,
        duration_seconds=track.duration_seconds,
        format=track.format,
        created_at=track.created_at.isoformat(),
    )
