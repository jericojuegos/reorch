# ⚡ Active Sprint: Phase 0 — Foundation

> **Objective:** Establish a stable, scalable backbone for audio jobs.
> **Context:** See [00-roadmap.md](./00-roadmap.md#-phase-0-foundation-pre-mvp) and [specify.md](./specify.md)

## 🚨 Critical Rules for This Sprint
* **Do NOT** build any audio processing logic yet — that's Phase 1.
* **MUST** use monorepo structure (`apps/`, `packages/`).
* **MUST** containerize all services (Docker Compose).
* **Update:** Mark tasks as `[x]` immediately upon verification.

---

## 🔄 Current Task (The Focus)
*The AI should only look here for the next step.*

- [x] **Project Initialization**
    - [x] Initialize Git repo with `git init`
    - [x] Create monorepo structure:
      ```
      reorch/
      ├── apps/
      │   ├── web/          # Next.js frontend
      │   └── api/          # FastAPI backend
      ├── packages/
      │   └── worker/       # Python audio pipeline worker
      ├── docker/
      │   └── docker-compose.yml
      └── .env.example
      ```
    - [x] Create root `README.md` with project overview
    - [x] Create `.gitignore` for Python + Node
    - [x] **Verify:** `git status` shows clean structure

---

## ⏳ Upcoming Tasks (On Deck)
*Queue for when the Current Task is done.*

### Frontend Scaffolding
- [x] Scaffold Next.js app in `apps/web/`
- [x] Install Tailwind CSS + shadcn/ui
- [x] Create placeholder landing page

### Backend Scaffolding
- [x] Scaffold FastAPI app in `apps/api/`
- [x] Add health check endpoint (`GET /health`)
- [x] Environment config with `.env` schema
- [ ] Connect to PostgreSQL

### Worker Scaffolding
- [x] Create worker skeleton in `packages/worker/`
- [x] Redis queue connection
- [x] Job polling loop skeleton

### Docker Environment
- [ ] Create `docker-compose.yml` with:
  - PostgreSQL 15
  - Redis 7
  - API service
  - Worker service
- [ ] Test `docker-compose up` successfully starts all services

---

## 🛑 Blocked / Waiting
*None currently.*

---

## 📝 Activity Log
- `2026-02-09` **Project Initialization completed** — monorepo structure, README, .gitignore, .env.example, docker-compose.yml.
- `2026-02-09` Consolidated project specification from ChatGPT reference.
- `2026-02-09` Aligned `.agent/` directory structure with template.
