# 🗺️ REORCH — Roadmap (`docs/planning/roadmap.md`)

> **Vision:** The premier AI-assisted platform for professional music re-orchestration and genre transformation.
> **North Star:** Users can seamlessly upload a track and transform its genre with incrementally better quality at each phase.

## 🧭 Legend
- `[x]` Completed · `[ ]` Pending · `[>]` **Current Focus** (Active Phase) · `[-]` Skipped/Deferred · `[!]` Blocked

---

## ✅ Phase 0: Foundation (Pre-MVP) — COMPLETE
*Goal: Establish a stable, scalable backbone for audio jobs.*

### Infrastructure & Core Concepts
- [x] Monorepo structure finalized (`apps/web`, `apps/api`, `packages/worker`)
- [x] Next.js frontend scaffolded
- [x] FastAPI backend scaffolded
- [x] Worker service initialized (separate process)
- [x] PostgreSQL schema created
- [x] Redis job queue wired
- [x] S3-compatible storage configured
- [x] Docker-based local dev environment
- [x] Job lifecycle model (`queued` → `running` → `succeeded`/`failed`)
- [x] Track ingestion & canonicalization (FFmpeg)
- [x] Preset-based processing config ("recipes")
- [x] Progress checkpoints & logging

---

## ✅ Phase 1: MVP — Re-Orchestration Core — COMPLETE
*Goal: Deliver a usable and reliable song transformation pipeline.*

### Audio Pipeline, Product Features & Guardrails
- [x] Upload audio (WAV/MP3) & convert to canonical WAV format
- [x] Basic analysis (tempo/BPM, duration)
- [x] One transformation preset: **Ballad → Rock**
- [x] Full-track (non-stem) processing: EQ, compression, saturation, loudness normalization
- [x] Final render (MP3 + WAV)
- [x] Create project, upload track, start re-orchestration job, view progress, download result
- [x] File size & duration limits, retry & timeout rules, clear failure messages

---

## [>] 💎 Phase 2: V1 — Quality Upgrade & Usability (ACTIVE)
*Goal: Improve musical quality with stem separation and give users more control over the transformation.*
*(Detailed task breakdown in [`docs/planning/01-active-sprint.md`](01-active-sprint.md))*

### Audio Enhancements (Completed in Sprint 2)
- [x] Stem separation (`vocals` / `drums` / `bass` / `other` via Demucs `htdemucs` in `pipeline/separate.py`)
- [x] Stem-aligned time-stretch (`pipeline/time_stretch.py` via `pyrubberband` with vocal formant preservation)
- [x] Improved drum energy for rock presets (`pipeline/stem_fx.py` with parallel compression + aggressive drum chain)
- [x] Better low-end control (`bass` Pedalboard chain + cross-stem sidechain ducking on drum envelope)
- [x] Cleaner vocal presence (HPF 80Hz, mud cut at 200Hz, presence boost at 3kHz, de-ess at 8kHz)
- [x] Improved mastering chain (`normalize.py` 2-pass LUFS normalization at -14 LUFS + -1.0 dBTP true peak ceiling)

### Presets (Next Up)
- [ ] Ballad → Rock (verify & finalize improved stem processing)
- [ ] Acoustic → Pop Punk (define pedalboard effects chain & test with acoustic guitar tracks)
- [ ] Chill → Upbeat (define pedalboard effects chain & test with lo-fi / ambient tracks)

### UX Improvements (Next Up)
- [ ] Preset intensity slider (`0.0–1.0` across Backend, Worker, and Frontend upload form)
- [ ] Job history per project (Backend query by project ID + Frontend project detail page)
- [ ] Output comparison (side-by-side original vs. re-orch audio player)
- [ ] Optional stem export (ZIP archive of stem files + "Download Stems" button)

---

## 🎵 Phase 3: Song Generation (Create Mode)
*Goal: Add controlled song generation without compromising REORCH's identity.*
- [ ] Prompt-based song generation (API or self-hosted) with optional lyrics, duration limits & style tags
- [ ] Generate → Re-Orchestrate → Export workflow
- [ ] Credit-based usage & per-user concurrency limits

---

## 🤖 Phase 4: AI Agent Layer
*Goal: Improve creative decision-making and output consistency.*
- [ ] Producer Agent (converts user intent into strict JSON recipe: presets, intensity, mix targets)
- [ ] QA / Refinement Agent (reviews LUFS, clipping, duration and triggers optional second-pass refinement)
- [ ] Cost-aware planning & allowed parameter range enforcement

---

## 🧊 Icebox (Future Ideas)
- [ ] Advanced structure detection (sections, fills, drops) & arrangement-level variation
- [ ] Multi-version batch export & API access for developers
- [ ] WebSocket job updates, email notifications, and preset marketplace
