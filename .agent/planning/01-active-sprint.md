# ⚡ Active Sprint: Phase 1 — MVP Re-Orchestration Core

> **Objective:** Deliver a usable and reliable song transformation pipeline.
> **Context:** See [00-roadmap.md](./00-roadmap.md#-phase-1-mvp--re-orchestration-core)

## 🚨 Critical Rules for This Sprint
* **Focus on end-to-end flow** — Upload → Process → Download must work.
* **Single preset only** — Ballad → Rock transformation.
* **No stem separation yet** — Full-track processing only (Phase 2).
* **Update:** Mark tasks as `[x]` immediately upon verification.

---

## 🔄 Current Task (The Focus)
*The AI should only look here for the next step, unless an **AD-HOC TASK** is explicitly requested.*

- [x] **Frontend Integration**
    - [x] **Upload Track UI**
        - [x] Create upload form component with drag-and-drop
        - [x] Integrate with `/api/tracks` POST endpoint
        - [x] Display upload progress
        - [x] Handle file validation errors
    - [x] **Job Progress Display**
        - [x] Create job status component
        - [x] Implement polling for job updates
        - [x] Display progress percentage and stage name
        - [x] Show error messages if job fails
    - [x] **Download Result Button**
        - [x] Generate signed S3 URLs for WAV/MP3
        - [x] Create download UI with format selection
        - [x] Handle download errors gracefully

---

## 🐛 Ad-Hoc / Side Quests
*Quick tweaks, UI experiments, or "Side Quests" that are NOT part of the main sprint objective. Log them here to keep the history clean.*

- [x] `2026-02-21`: (Agent) Refined `atomic-rules.md` and `budget-guard.md` based on Gemini/Claude review feedback.
- [ ] *(Agent: log future ad-hoc tasks here)*

---

## ⏳ Upcoming Tasks (On Deck)

### Guardrails & Error Handling
- [ ] File size & duration limits
- [ ] Retry & timeout rules
- [ ] Clear failure messages

---

## 🛑 Blocked / Waiting
*None currently.*

---

## 📝 Activity Log
- `2026-02-21` **Frontend Integration completed.** Created `UploadTrack` drag-and-drop component, integrated with `/api/tracks` using XMLHttpRequest for upload progress. Added `JobProgress` component for polling `/api/jobs/{job_id}` and displaying visual stage feedback. Integrated `s3_client.generate_presigned_url` into the backend to power the final WAV/MP3 download buttons.
- `2026-02-21` **Agent rules and loop protocols refined.** Integrated Claude's suggestions into `atomic-rules.md` and `budget-guard.md`. Improved recovery protocols, command tiering, and verification failure paths. Updated `README.md`.
- `2026-02-17` **Landing Page UI Redesign completed.** Implemented a modern, dark-themed landing page with full-screen hero section, custom Tailwind v4 configuration, and Outfit/Inter fonts. Verified with build + manual dev server check.
- `2026-02-13` **Audio Processing Pipeline completed.** Implemented 5-stage pipeline (canonicalize, analyze, transform, normalize, render) with FFmpeg + pedalboard DSP. Verified with integration tests in Docker. All 7 tests passed.
- `2026-02-12` Job Queue Integration completed. Fixed asyncpg enum binding + timezone-naive datetime issues. E2E verified: queued → running → succeeded with progress polling.
- `2026-02-12` Track Upload & Storage completed. POST /tracks with S3 upload and validation verified.
- `2026-02-11` Database Schema & Models completed. Alembic migrations set up, verified upgrade/downgrade cycle and API CRUD.
- `2026-02-09` Phase 1 sprint started after Phase 0 completion.

