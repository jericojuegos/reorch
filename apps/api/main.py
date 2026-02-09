"""
REORCH API - FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="REORCH API",
    description="Backend API for the REORCH music re-orchestration platform",
    version="0.1.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
