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
*The AI should only look here for the next step.*

- [ ] **Job Queue Integration**
    - [ ] API enqueues jobs to Redis
    - [ ] Worker polls and claims jobs
    - [ ] Update job status in database
    - [ ] Progress reporting (percentage)

---

## ⏳ Upcoming Tasks (On Deck)

### Audio Processing Pipeline
- [ ] FFmpeg canonicalization (convert to WAV 44.1kHz 16-bit)
- [ ] Basic analysis (tempo/BPM, duration)
- [ ] Ballad → Rock preset (EQ, compression, saturation)
- [ ] Loudness normalization (LUFS)
- [ ] Final render (MP3 + WAV)

### Frontend Integration
- [ ] Upload track UI
- [ ] Job progress display
- [ ] Download result button

---

## 🛑 Blocked / Waiting
*None currently.*

---

## 📝 Activity Log
- `2026-02-12` Track Upload & Storage completed. POST /tracks with S3 upload and validation verified.
- `2026-02-11` Database Schema & Models completed. Alembic migrations set up, verified upgrade/downgrade cycle and API CRUD.
- `2026-02-09` Phase 1 sprint started after Phase 0 completion.

