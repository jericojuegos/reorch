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

- [ ] **Frontend Integration**
    - [ ] **Upload Track UI**
        - [ ] Create upload form component with drag-and-drop
        - [ ] Integrate with `/api/tracks` POST endpoint
        - [ ] Display upload progress
        - [ ] Handle file validation errors
    - [ ] **Job Progress Display**
        - [ ] Create job status component
        - [ ] Implement polling for job updates
        - [ ] Display progress percentage and stage name
        - [ ] Show error messages if job fails
    - [ ] **Download Result Button**
        - [ ] Generate signed S3 URLs for WAV/MP3
        - [ ] Create download UI with format selection
        - [ ] Handle download errors gracefully

---

## 🐛 Ad-Hoc / Side Quests
*Quick tweaks, UI experiments, or "Side Quests" that are NOT part of the main sprint objective. Log them here to keep the history clean.*

- [x] `2026-02-17`: (Web) Implemented new landing page design with full-screen hero and Tailwind v4 config.
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
- `2026-02-17` **Landing Page UI Redesign completed.** Implemented a modern, dark-themed landing page with full-screen hero section, custom Tailwind v4 configuration, and Outfit/Inter fonts. Verified with build + manual dev server check.
- `2026-02-13` **Audio Processing Pipeline completed.** Implemented 5-stage pipeline (canonicalize, analyze, transform, normalize, render) with FFmpeg + pedalboard DSP. Verified with integration tests in Docker. All 7 tests passed.
- `2026-02-12` Job Queue Integration completed. Fixed asyncpg enum binding + timezone-naive datetime issues. E2E verified: queued → running → succeeded with progress polling.
- `2026-02-12` Track Upload & Storage completed. POST /tracks with S3 upload and validation verified.
- `2026-02-11` Database Schema & Models completed. Alembic migrations set up, verified upgrade/downgrade cycle and API CRUD.
- `2026-02-09` Phase 1 sprint started after Phase 0 completion.

