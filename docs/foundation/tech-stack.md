# REORCH Tech Stack

> Approved technologies and conventions for REORCH development.

---

## Frontend

| Category | Technology | Notes |
|----------|------------|-------|
| **Framework** | Next.js 14+ (App Router) | TypeScript, Server Components |
| **Styling** | Tailwind CSS + shadcn/ui | Dark theme, studio aesthetic |
| **Audio** | Web Audio API + wavesurfer.js | Waveform visualization, playback |
| **State** | React Context + TanStack Query | Server state via React Query |
| **Forms** | React Hook Form + Zod | Validation |

---

## Backend (API)

| Category | Technology | Notes |
|----------|------------|-------|
| **Framework** | FastAPI (Python 3.11+) | Async, Pydantic models |
| **Auth** | JWT (via frontend provider) | Stateless token validation |
| **ORM** | SQLAlchemy 2.0 | Async sessions |
| **Migrations** | Alembic | Version-controlled schema |
| **Validation** | Pydantic v2 | Request/response schemas |

---

## Worker (Audio Pipeline)

| Category | Technology | Notes |
|----------|------------|-------|
| **Runtime** | Python 3.11+ | Separate process from API |
| **Queue** | Redis (RQ or custom) | Job polling |
| **Audio Processing** | FFmpeg, pydub, librosa | Format conversion, analysis |
| **Stem Separation** | Demucs / Spleeter | V1+ (optional GPU) |
| **Mastering** | pyloudnorm, pedalboard | LUFS normalization, effects |

---

## Infrastructure

| Category | Technology | Notes |
|----------|------------|-------|
| **Database** | PostgreSQL 15+ | Primary data store |
| **Cache/Queue** | Redis 7+ | Job queue, optional caching |
| **Storage** | S3-compatible | Cloudflare R2, MinIO, or AWS S3 |
| **Containers** | Docker + Docker Compose | Local dev environment |
| **CI/CD** | GitHub Actions | Lint, test, deploy |

---

## Conventions

### Code Style
- **Python:** Black, Ruff, isort
- **TypeScript:** ESLint, Prettier

### Naming
- **API Routes:** `/v1/<resource>` (RESTful)
- **DB Tables:** snake_case, plural (`users`, `jobs`)
- **React Components:** PascalCase
- **CSS Classes:** Tailwind utilities or BEM for custom

### Environment
- Use `.env` files (never commit secrets)
- Schema: `ENV`, `DATABASE_URL`, `REDIS_URL`, `S3_ENDPOINT`, `S3_BUCKET`, etc.

---

## Prohibited

| ❌ Avoid | Reason |
|----------|--------|
| Direct DB access from frontend | Security, architecture boundary |
| Streaming audio through API | Use signed S3 URLs instead |
| Synchronous long-running requests | Use job queue for audio processing |
| Celebrity voice cloning | Legal/ethical risk |
