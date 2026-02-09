"""
Projects API router.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Project


router = APIRouter()


# === Schemas ===

class ProjectCreate(BaseModel):
    """Schema for creating a project."""
    name: str
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# === Endpoints ===

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new project."""
    db_project = Project(
        name=project.name,
        description=project.description,
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return ProjectResponse(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        created_at=db_project.created_at.isoformat(),
        updated_at=db_project.updated_at.isoformat(),
    )


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
):
    """List all projects."""
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            created_at=p.created_at.isoformat(),
            updated_at=p.updated_at.isoformat(),
        )
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a project by ID."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )
