# 📜 Sprint History

> Complete execution log of all completed phases and sprints. For the high-level vision, see [00-roadmap.md](./00-roadmap.md).

---

## ✅ Phase 0 — Foundation / Pre-MVP (Completed 2026-02-09)

### Infrastructure
- [x] Monorepo structure finalized (`apps/web`, `apps/api`, `packages/worker`)
- [x] Next.js frontend scaffolded
- [x] FastAPI backend scaffolded
- [x] Worker service initialized (separate Python process)
- [x] Redis job queue wired (`job_queue.py` + `queue_client.py`)
- [x] S3-compatible storage configured (MinIO via `aioboto3`)
- [x] Docker-based local dev environment (`docker/docker-compose.yml`)

### Activity Log
- `2026-02-09` Phase 0 completed. All infrastructure in place.

---

## ✅ Phase 1 — MVP Re-Orchestration Core (Completed 2026-02-21)

### Database & API
- [x] PostgreSQL schema (Projects, Tracks, Jobs) with Alembic migrations
- [x] `POST /projects` — create project
- [x] `POST /tracks` — upload audio with S3 storage, file validation, duration extraction (mutagen)
- [x] `POST /jobs` — enqueue processing job to Redis
- [x] `GET /jobs/{id}` — poll job status and progress
- [x] `GET /jobs/{id}/download` — generate presigned S3 download URLs

### Audio Processing Pipeline (Worker)
- [x] 5-stage pipeline: Canonicalize → Analyze → Transform → Normalize → Render
- [x] Canonicalize: FFmpeg conversion to 44.1kHz 16-bit WAV
- [x] Analyze: Duration + BPM estimation (numpy onset detection)
- [x] Transform: `ballad_to_rock` preset (EQ, compression, distortion via Pedalboard)
- [x] Normalize: LUFS loudness normalization
- [x] Render: Final WAV + MP3 export, upload to S3

### Frontend
- [x] Landing page (dark theme, hero section, Tailwind v4, Outfit/Inter fonts)
- [x] Upload Track UI (drag-and-drop via `react-dropzone`, XMLHttpRequest progress)
- [x] Job Progress Display (2s polling, stage names, visual progress bar)
- [x] Download Result buttons (WAV/MP3 via presigned S3 URLs)

### Guardrails & Error Handling
- [x] File size limit: 50MB (frontend) / 100MB (backend)
- [x] Duration limit: 10 minutes (mutagen-based validation)
- [x] Worker retry logic: max 3 attempts with automatic requeue
- [x] Worker timeout: 15-minute `asyncio.wait_for` on pipeline execution
- [x] Error message propagation: worker exceptions → DB `error_message` → UI red banner

### Bug Fixes (During Testing)
- [x] Fixed trailing slash routing bug (FastAPI 307 redirect breaking multipart uploads)
- [x] Fixed Docker cache not picking up new `mutagen` dependency
- [x] Fixed presigned URL using Docker-internal `minio:9000` instead of `localhost:9000`
- [x] Removed accidental test exception left in `analyze.py`

### Ad-Hoc / Side Quests
- [x] `2026-02-21`: Refined `atomic-rules.md` and `budget-guard.md`

### Activity Log
- `2026-02-21` Phase 1 fully tested end-to-end by user. Download working.
- `2026-02-21` Guardrails & Error Handling completed.
- `2026-02-21` Frontend Integration completed.
- `2026-02-21` Agent rules and loop protocols refined.
- `2026-02-17` Landing Page UI Redesign completed.
- `2026-02-13` Audio Processing Pipeline completed (7 integration tests passed).
- `2026-02-12` Job Queue Integration completed.
- `2026-02-12` Track Upload & Storage completed.
- `2026-02-11` Database Schema & Models completed.
- `2026-02-09` Phase 1 sprint started.
