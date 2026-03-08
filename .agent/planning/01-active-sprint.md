# ⚡ Active Sprint: Phase 2 — V1 Quality Upgrade & Usability

> **Objective:** Improve musical quality with stem separation and give users more control over the transformation.
> **Context:** See [00-roadmap.md](./00-roadmap.md)

## 🚨 Critical Rules for This Sprint
* **Stem separation is the core upgrade** — isolate vocals, drums, bass, other.
* **Improve the Ballad → Rock preset** before adding new ones.
* **UX upgrades** — users need comparison and control tools.
* **Update:** Mark tasks as `[x]` immediately upon verification.

---

## 🔄 Current Task (The Focus)
*The AI should only look here for the next step, unless an **AD-HOC TASK** is explicitly requested.*

- [ ] **Audio Enhancements**
    - [x] Stem separation (vocals / drums / bass / other)
        - [x] Research & integrate Demucs (or similar) into worker pipeline
        - [x] Add `separate` stage between `canonicalize` and `analyze`
        - [x] Store individual stem files in S3
        - [x] Update `AnalysisResult` to include per-stem metadata
    - [x] Stem-aligned time-stretch
        - [x] Implement tempo adjustment per-stem
        - [x] Preserve vocal pitch during stretch
    - [x] Improved drum energy for rock presets
        - [x] Apply heavier compression + saturation to drum stem
        - [x] Add parallel compression for punch
    - [x] Better low-end control (bass)
        - [x] Sidechain-style ducking on bass stem
        - [x] Sub-bass enhancement filter
    - [x] Cleaner vocal presence
        - [x] De-ess and mid-range boost on vocal stem
        - [x] Reduce muddiness with surgical EQ
    - [x] Improved mastering chain (LUFS + true peak)
        - [x] Add true peak limiter to render stage
        - [x] Target -14 LUFS for streaming

---

## ⏳ Upcoming Tasks (On Deck)

### New Presets
- [ ] Ballad → Rock (improved with stem processing)
- [ ] Acoustic → Pop Punk
    - [ ] Define pedalboard effects chain
    - [ ] Test with acoustic guitar tracks
- [ ] Chill → Upbeat
    - [ ] Define pedalboard effects chain
    - [ ] Test with lo-fi / ambient tracks

### UX Improvements
- [ ] Preset intensity slider
    - [ ] Backend: accept `intensity` param (0.0–1.0) in job creation
    - [ ] Frontend: add slider component to upload form
    - [ ] Worker: scale effect gains by intensity factor
- [ ] Job history per project
    - [ ] Backend: query jobs by project ID
    - [ ] Frontend: project detail page with job list
- [ ] Output comparison (original vs re-orch)
    - [ ] Frontend: side-by-side audio player component
    - [ ] Backend: return both original and output presigned URLs
- [ ] Optional stem export (ZIP)
    - [ ] Backend: create ZIP archive of stem files
    - [ ] Frontend: add "Download Stems" button

---

## 🐛 Ad-Hoc / Side Quests
*Quick tweaks, UI experiments, or "Side Quests" that are NOT part of the main sprint objective.*

- [ ] *(Agent: log future ad-hoc tasks here)*

---

## 🛑 Blocked / Waiting
*None currently.*

---

## 📝 Activity Log
- `2026-03-08` **Improved mastering chain.** Upgraded `normalize.py` to 2-pass mastering: LUFS normalization (−14 LUFS via pyloudnorm) + brickwall true peak ceiling clamp (−1.0 dBTP). Replaced naive amplitude clamp with proportional scaling.
- `2026-03-08` **Cleaner vocal presence.** Added vocal Pedalboard chain to `ballad_to_rock`: HPF 80Hz, -2.5dB mud cut at 200Hz, +3.5dB presence boost at 3kHz, -3dB de-ess at 8kHz, gentle 2.5:1 compression.
- `2026-03-08` **Better low-end control (bass).** Added bass Pedalboard chain (+4dB sub-bass shelf, HPF 30Hz, 3:1 comp), cross-stem sidechain ducking (bass ducks on drum envelope, 50% depth), `SidechainConfig` dataclass.
- `2026-03-08` **Improved drum energy for rock presets.** Created `pipeline/stem_fx.py` with per-stem pedalboard chains, parallel compression (60% wet), aggressive drum chain (6:1 comp, 12dB drive, 5kHz snap), wired as Stage 3c.
- `2026-03-08` **Stem-aligned time-stretch implemented.** Created `pipeline/time_stretch.py` (pyrubberband wrapper with vocal formant preservation), updated pipeline to 7-stage flow with remix, added per-stem mock-based tests.
- `2026-03-02` **Stem separation integrated.** Created `pipeline/separate.py` (Demucs htdemucs wrapper), updated pipeline to 6-stage flow, added per-stem metadata to `AnalysisResult`, S3 stem upload in `main.py`, mock-based tests.
- `2026-02-21` **Phase 2 sprint board created.** Migrated from Phase 1 (completed). Archived Phase 1 tasks to `03-history.md`. Exploded Phase 2 roadmap items into technical sub-tasks.
