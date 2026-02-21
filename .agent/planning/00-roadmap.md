# 🗺️ REORCH Roadmap

> **Vision:** The premier AI-assisted platform for professional music re-orchestration and genre transformation.
> **North Star:** Users can seamlessly upload a track and transform its genre with incrementally better quality at each phase.

## 📌 Legend
- `[x]` Completed
- `[ ]` Pending
- `[>]` **Current Focus** (Active Phase)
- `[-]` Skipped/Deferred
- `[!]` Blocked

---

## ✅ Phase 0: Foundation (Pre-MVP) — COMPLETE
*Goal: Establish a stable, scalable backbone for audio jobs.*

### Infrastructure
- [x] Monorepo structure finalized
- [x] Next.js frontend scaffolded
- [x] FastAPI backend scaffolded
- [x] Worker service initialized (separate process)
- [ ] PostgreSQL schema created *(deferred to Phase 1)*
- [x] Redis job queue wired
- [x] S3-compatible storage configured
- [x] Docker-based local dev environment

### Core Concepts
- [ ] Job lifecycle model (queued → running → succeeded/failed) *(Phase 1)*
- [ ] Track ingestion & canonicalization (FFmpeg) *(Phase 1)*
- [ ] Preset-based processing config ("recipes") *(Phase 1)*
- [ ] Progress checkpoints & logging *(Phase 1)*

---

## ✅ Phase 1: MVP — Re-Orchestration Core — COMPLETE
*Goal: Deliver a usable and reliable song transformation pipeline.*

### Audio Pipeline (MVP Quality)
- [x] Upload audio (WAV/MP3)
- [x] Convert to canonical WAV format
- [x] Basic analysis (tempo/BPM, duration)
- [x] One transformation preset: **Ballad → Rock**
- [x] Full-track (non-stem) processing: EQ, compression, saturation, loudness normalization
- [x] Final render (MP3 + WAV)

### Product Features
- [x] Create project
- [x] Upload track
- [x] Start re-orchestration job
- [x] View job progress
- [x] Download result

### Guardrails
- [x] File size & duration limits
- [x] Retry & timeout rules
- [x] Clear failure messages

---

## [>] 💅 Phase 2: V1 — Quality Upgrade & Usability
*Goal: Improve musical quality and user control.*

### Audio Enhancements
- [ ] Stem separation (vocals / drums / bass / other)
- [ ] Stem-aligned time-stretch
- [ ] Improved drum energy for rock presets
- [ ] Better low-end control (bass)
- [ ] Cleaner vocal presence
- [ ] Improved mastering chain (LUFS + true peak)

### Presets
- [ ] Ballad → Rock (improved)
- [ ] Acoustic → Pop Punk
- [ ] Chill → Upbeat

### UX
- [ ] Preset intensity slider
- [ ] Job history per project
- [ ] Output comparison (original vs re-orch)
- [ ] Optional stem export (ZIP)

---

## 🎤 Phase 3: Song Generation (Create Mode)
*Goal: Add controlled song generation without compromising REORCH's identity.*

### Generation Pipeline
- [ ] Prompt-based song generation (API or self-hosted)
- [ ] Optional lyrics input
- [ ] Duration limits & style tags
- [ ] Generation jobs use same queue + storage system

### Workflow
- [ ] Generate → Re-Orchestrate → Export
- [ ] Re-use re-orch presets on generated songs

### Cost Control
- [ ] Credit-based usage
- [ ] Generation priced higher than re-orch
- [ ] Per-user concurrency limits

---

## 🤖 Phase 4: AI Agent Layer (Optional, High ROI)
*Goal: Improve creative decision-making and output consistency.*

### Producer Agent
- [ ] Converts user intent into a structured "recipe"
- [ ] Selects presets, intensity, mix targets
- [ ] Outputs strict JSON only

### QA / Refinement Agent
- [ ] Reviews metrics (LUFS, clipping, duration)
- [ ] Triggers optional second-pass refinement

### Safety
- [ ] Cost-aware planning
- [ ] Allowed parameter ranges enforced
- [ ] No direct DSP execution by agents

---

## 🧊 Icebox (Future Ideas)
*Tasks we might do later, but not for MVP.*
- [ ] Advanced structure detection (sections, fills, drops)
- [ ] Arrangement-level variation
- [ ] Multi-version batch export
- [ ] API access for developers
- [ ] Plugin / integration clients (WordPress, DAWs)
- [ ] WebSocket job updates
- [ ] Email notifications
- [ ] Preset marketplace
