# REORCH Architecture

> System design and service boundaries for the REORCH platform.

---

## Service Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│  Next.js (TypeScript) — SSR + Client Components                │
│  - Landing Page, Upload UI, Job Dashboard, Audio Player         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API
┌──────────────────────────▼──────────────────────────────────────┐
│                         API SERVICE                             │
│  FastAPI (Python) — Stateless REST                              │
│  - Auth, Project/Track CRUD, Job Creation, Signed URLs          │
└────────┬─────────────────┬─────────────────┬────────────────────┘
         │                 │                 │
         ▼                 ▼                 ▼
┌────────────────┐ ┌───────────────┐ ┌────────────────────────────┐
│   PostgreSQL   │ │     Redis     │ │   S3 (Object Storage)      │
│   (Core Data)  │ │ (Job Queue)   │ │   uploads/, outputs/       │
└────────────────┘ └───────┬───────┘ └────────────────────────────┘
                           │ Job Poll
┌──────────────────────────▼──────────────────────────────────────┐
│                       WORKER SERVICE                            │
│  Python — Audio Pipeline Executor                               │
│  - Ingest, Analyze, Separate, Re-Orch, Master, Upload           │
│  - Horizontally scalable (N workers)                            │
│  - Optional GPU for stem separation models                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

1. **Upload:** User → Frontend → API (signed URL) → S3 (original)
2. **Job Creation:** API → PostgreSQL (job record) → Redis (enqueue)
3. **Processing:** Worker (poll Redis) → S3 (download) → Pipeline → S3 (upload outputs)
4. **Status:** Worker → PostgreSQL (progress updates) ← Frontend (poll API)
5. **Download:** User → API (signed URL) → S3 (outputs)

---

## Key Boundaries

| Boundary | Responsibility |
|----------|----------------|
| **Frontend ↔ API** | REST only. No direct DB/Redis access from frontend. |
| **API ↔ Worker** | Communicate via Redis queue + Postgres state. No direct calls. |
| **Worker ↔ Storage** | Workers read/write S3 directly (download/upload audio). |
| **API ↔ Storage** | API generates signed URLs only. No file streaming through API. |

---

## Job Lifecycle

```
queued → running → succeeded
                 ↘ failed
```

- **Idempotent:** Retries must not duplicate outputs.
- **Timeouts:** Per-stage limits prevent zombie jobs.
- **Progress Checkpoints:** 0–10% ingest, 10–25% analysis, 25–60% separation, 60–85% reorch, 85–95% master, 95–100% finalize.

---

## Scaling Considerations

| Component | Strategy |
|-----------|----------|
| **Frontend** | Vercel/Cloudflare (edge) or self-hosted containers |
| **API** | Stateless, scale horizontally behind load balancer |
| **Workers** | N workers polling same Redis queue; add GPU nodes for heavy models |
| **Storage** | S3-compatible (Cloudflare R2, MinIO, AWS S3) with lifecycle policies |

---

## Future Extensions

- **WebSocket:** Real-time job progress (replace polling)
- **AI Agents:** Producer/QA agents as separate microservices
- **Plugin API:** External integrations (DAWs, WordPress)
