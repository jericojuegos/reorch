# REORCH — Action Items

> Concrete, executable tasks. Intentionally tactical and implementation-focused.

---

## Immediate (Week 1–2)

### Repo & Setup
- [ ] Create repo with: README.md, ROADMAP.md, ACTION_ITEMS.md, specify.md
- [ ] Decide repo structure (mono vs split)
- [ ] Add Docker config for: API, Worker, Postgres, Redis

### Backend
- [ ] Scaffold FastAPI app
- [ ] Health check endpoint
- [ ] Environment config (.env schema)
- [ ] Connect Postgres
- [ ] Create base models: User, Project, Track, Job, Output

### Worker
- [ ] Worker process skeleton
- [ ] Redis queue connection
- [ ] Job polling loop
- [ ] Logging + error capture

---

## Short-Term (MVP Completion)

### Audio Pipeline
- [ ] FFmpeg wrapper utilities
- [ ] Canonical WAV conversion
- [ ] Duration + loudness analysis
- [ ] Implement Ballad → Rock preset (full-track)
- [ ] Render output files
- [ ] Upload outputs to storage

### Job System
- [ ] Job creation API
- [ ] Job progress updates
- [ ] Job status polling
- [ ] Failure handling + retries

### Frontend
- [ ] Landing page (temporary)
- [ ] Upload UI
- [ ] Job progress UI
- [ ] Download links

---

## Mid-Term (V1 Quality)

### Audio
- [ ] Evaluate stem separation options
- [ ] Integrate stem separation
- [ ] Stem alignment & mixing
- [ ] Preset tuning & intensity scaling

### UX
- [ ] Preset selector
- [ ] Intensity slider
- [ ] Project/job history view
- [ ] Compare original vs re-orch

---

## Generation Mode Prep

- [ ] Define generation job schema
- [ ] Decide provider vs self-hosted
- [ ] Add generation job type
- [ ] UI for prompt + options
- [ ] Credit accounting logic

---

## AI Agent Prep (No Implementation Yet)

- [ ] Define "recipe" JSON schema
- [ ] Add recipe column to jobs
- [ ] Log audio metrics consistently
- [ ] Add second-pass pipeline hook

---

## Non-Code (Important)

- [ ] Define audio retention policy
- [ ] Add user rights confirmation copy
- [ ] Document known limitations clearly
- [ ] Create cost tracking dashboard (basic)

---

## Guiding Rule

> If a task increases reliability → prioritize  
> If it improves audio quality incrementally → good  
> If it adds hype without control → delay  
> 
> **Build REORCH like a studio tool, not a demo.**
