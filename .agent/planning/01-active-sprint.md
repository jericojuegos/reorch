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

- [x] **Audio Processing Pipeline** *(code complete — verify verified in Docker)*
    - [x] FFmpeg canonicalization (convert to WAV 44.1kHz 16-bit)
    - [x] Basic analysis (tempo/BPM, duration)
    - [x] Ballad → Rock preset (EQ, compression, saturation)
    - [x] Loudness normalization (LUFS)
    - [x] Final render (MP3 + WAV)
    - [x] Run `pytest tests/test_pipeline.py` (Verified in Docker)

---

## ⏳ Upcoming Tasks (On Deck)

### Frontend Integration
- [ ] Upload track UI
- [ ] Job progress display
- [ ] Download result button

---

## 🛑 Blocked / Waiting
*None currently.*

---

## 📝 Activity Log
- `2026-02-12` Job Queue Integration completed. Fixed asyncpg enum binding + timezone-naive datetime issues. E2E verified: queued → running → succeeded with progress polling.
- `2026-02-12` Track Upload & Storage completed. POST /tracks with S3 upload and validation verified.
- `2026-02-11` Database Schema & Models completed. Alembic migrations set up, verified upgrade/downgrade cycle and API CRUD.
- `2026-02-09` Phase 1 sprint started after Phase 0 completion.

