# 🎵 REORCH

> The premier AI-assisted platform for professional music re-orchestration and genre transformation.

## Overview

REORCH enables users to seamlessly upload a track and transform its genre with incrementally better quality at each phase. The platform leverages modern audio processing pipelines and AI-driven presets to deliver professional-grade re-orchestrations.

## Project Structure

```
reorch/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # FastAPI backend
├── packages/
│   └── worker/       # Python audio pipeline worker
├── docker/
│   └── docker-compose.yml
├── .agent/           # AI assistant configuration
└── .env.example
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js, Tailwind CSS, shadcn/ui |
| Backend | FastAPI (Python 3.11+) |
| Worker | Python, Redis Queue |
| Database | PostgreSQL 15 |
| Queue | Redis 7 |
| Storage | S3-compatible (MinIO for local dev) |
| Container | Docker, Docker Compose |

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- pnpm (for frontend)
