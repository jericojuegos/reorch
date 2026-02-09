"""
REORCH API - FastAPI Backend
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Initialize database tables
    await init_db()
    yield
    # Shutdown: Cleanup if needed


app = FastAPI(
    title="REORCH API",
    description="Backend API for the REORCH music re-orchestration platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import and include routers
from routers import jobs, projects

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    return {"status": "healthy", "service": "reorch-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to REORCH API",
        "docs": "/docs",
        "health": "/health",
    }
