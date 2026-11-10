# 🧠 REORCH — Agent Brain (`AGENTS.md`)

**Project:** REORCH — AI-Assisted Audio Re-Orchestration & Genre Transformation Monorepo
**Context:** Personal / Standalone
**Backend & Worker Stack:** Python 3.11+ · FastAPI (`apps/api`) · SQLAlchemy 2.0 (Async) · Alembic · PostgreSQL 15+ · Redis Queue · Worker (`packages/worker`: FFmpeg, Demucs, Pedalboard, Pyrubberband, Pyloudnorm) · S3-Compatible Storage
**Frontend Stack:** Next.js 14+ App Router (`apps/web`) · TypeScript · Tailwind CSS + shadcn/ui · Web Audio API + wavesurfer.js · TanStack Query
**Architecture Pattern:** Polyglot Monorepo (Next.js Web + FastAPI REST API + Async Audio DSP Worker)
**Master Brain:** `python-fastapi,nextjs-supabase`
**Last synced:** `python-fastapi+nextjs-supabase-v1.0` - 2026-11-10

---

## 🚦 Project State

**Stage:** `active` (Phase 2: V1 Quality Upgrade & Usability — Audio Enhancements complete, Presets & UX next)
**Stage last updated:** `2026-11-09`

| Stage | Meaning | Next Action / Skill |
|-------|---------|---------------------|
| `active` | Feature wave development in progress | **`/next`** → **`/spec`** → **`/build`** → **`/verify`** → **`/ship`** |

---

## ⚡ Deterministic Verification Commands

Run these commands after every task before marking `[x]`:
- **Frontend Build & Typecheck:** `npm run build` (`npm run build --prefix apps/web`)
- **Frontend Lint:** `npm run lint` (`npm run lint --prefix apps/web`)
- **Backend / Worker Tests:** `pytest` (run inside `apps/api` or `packages/worker`)

---

## 🗺️ Context Map (`docs/INDEX.md`) & Skills (`.agents/skills/`)

> **Progressive Disclosure Rule:** Do not read all docs at once. Read [`docs/INDEX.md`](docs/INDEX.md) or use this quick table:

| Question / Action | File or Skill |
|-------------------|---------------|
| What should I work on next? | **`/next`** ([`.agents/skills/next/SKILL.md`](.agents/skills/next/SKILL.md)) |
| What is the phased roadmap & current sprint status? | [`docs/planning/roadmap.md`](docs/planning/roadmap.md) & [`docs/planning/01-active-sprint.md`](docs/planning/01-active-sprint.md) |
| Create or expand a feature spec (`requirements`, `design`, `tasks`, `uat`) | **`/spec`** ([`.agents/skills/spec/SKILL.md`](.agents/skills/spec/SKILL.md)) |
| Build features or execute tasks/waves | **`/build`** ([`.agents/skills/build/SKILL.md`](.agents/skills/build/SKILL.md)) |
| Verify acceptance criteria, types, and quality standards | **`/verify`** ([`.agents/skills/verify/SKILL.md`](.agents/skills/verify/SKILL.md)) |
| Ship completed feature, update `roadmap.md`, and generate PR summary | **`/ship`** ([`.agents/skills/ship/SKILL.md`](.agents/skills/ship/SKILL.md)) |
| What are we building overall & why? | [`docs/foundation/prd.md`](docs/foundation/prd.md) |
| Where do files live & how does the audio pipeline work? | [`docs/foundation/architecture.md`](docs/foundation/architecture.md) |
| What packages, conventions & stack layers exist? | [`docs/foundation/tech-stack.md`](docs/foundation/tech-stack.md) |
| How do we execute tasks, waves & cross-model reviews? | [`.agents/rules/execution-protocol.md`](.agents/rules/execution-protocol.md) |
| What are the Python FastAPI & Next.js stack rules? | [`.agents/rules/stack-rules.md`](.agents/rules/stack-rules.md) |

---

## ⚠️ Critical Constraints — Never Violate

- **No Direct DB Access from Frontend:** All database operations go through `apps/api` (`/v1/*` endpoints) using SQLAlchemy 2.0 async parameterized queries and Alembic migrations.
- **No Synchronous Audio Processing in API:** All audio ingestion, stem separation, time-stretching, DSP effects, and mastering must execute asynchronously in `packages/worker` via the Redis job queue.
- **No Streaming Audio Through API:** All audio uploads and output/stem downloads must use time-limited presigned S3 URLs. Never expose internal bucket paths to clients.
- **Strict Upload Validation:** Validate both MIME type and magic bytes on audio uploads; enforce max file size (100MB) and max duration (10 minutes). Never execute user-uploaded files.
- **Auth & Security Hygiene:** Validate inputs server-side first (Pydantic v2 in Python, Zod in TypeScript). Store JWT tokens in `httpOnly` cookies only, never expose stack traces in API responses, and never commit secrets.
- **No Celebrity Voice Cloning:** Prohibited across all presets and generation modes for legal and ethical compliance.

---

## 🛡️ Code Review & Security Audit Gate (All AI Models)

When asked to review code, audit security, or evaluate another AI model's findings (even without invoking `/verify`):
1. **Contract First:** Read `docs/foundation/architecture.md`, `.agents/rules/stack-rules.md`, and the active feature's spec before flagging issues. Never contradict settled decisions or Non-Goals.
2. **Evidence-Only Severity Tiers (No Ping-Pong):** Only report **`[P0 — Blocker]`** and **`[P1 — Defect]`** with exact `file:line` and a concrete trigger path. Suppress **`[P2 — Style/Nitpick]`** opinions.
3. **Arbiter Mode for External Reviews:** Classify external findings against `design.md` + `stack-rules.md` into **`ACCEPT (P0/P1)`** vs. **`REJECT (P2 / Settled Tradeoff / Guarded Upstream)`** before modifying any code.

---

## 🚫 Anti-Hallucination List (Out of Scope for Current Phase)

Do NOT build in Phase 2 (V1):
- No prompt-based text-to-song generation (Phase 3)
- No AI Producer / QA Agent layer (Phase 4)
- No celebrity voice cloning (Never)
- No direct DSP execution by LLM agents
