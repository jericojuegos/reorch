---
trigger: always_on
globs: "**/*.py, pyproject.toml, requirements*.txt"
description: Python 3.12+ + uv + FastAPI + Pydantic v2 + SQLAlchemy/Supabase (Modular Domain Architecture) boundaries, coding standards, and pre-commit checklist
---

# 🏗️ Stack Rules: Python + FastAPI (`python-fastapi`)

---

## 1. Folder Responsibilities & Layer Boundaries (Modular Domain Architecture)

This stack uses **Modular Domain Architecture** — each domain feature lives in its own isolated package (`app/modules/[domain]/`) so parallel developers and AI subagents never collide.

### Folder Map

| Path | What Lives Here | What NEVER Lives Here |
|------|-----------------|-----------------------|
| `app/main.py` | FastAPI app initialization, lifespan hooks, CORS/middleware, router mounting | Business logic, DB queries, inline route implementations |
| `app/core/` | Config (`pydantic-settings`), DB session/engine, security/auth dependencies, shared AI/LLM clients | Domain-specific business logic |
| `app/modules/[domain]/` | Isolated domain slice: `router.py` (HTTP endpoints), `schemas.py` (Pydantic v2 models), `service.py` (business logic), `models.py` (DB models) | Imports from peer `app/modules/[other-domain]/` internals |
| `app/shared/` | Shared utilities, pagination schemas, base error classes | Route endpoints |
| `tests/[domain]/` | `pytest` unit & invariant tests (`test_*.py`) mapped to `Req X.Y` and `Property N` | Unmocked destructive production DB writes |

---

## 2. Mandatory 2026 Python & FastAPI Standards

1. **Dependency & Virtualenv Management (`uv` Only):** Always use `uv` (`uv add`, `uv run pytest`, `uv run ruff check`) — never run global `pip install`.
2. **Strict Type Hints Everywhere (Python 3.12+):** Every function signature, parameter, and return value must have explicit type annotations (`def create_item(payload: ItemCreate) -> ItemResponse:`).
3. **Pydantic v2 Validation:** Use Pydantic v2 (`model_validate`, `ConfigDict(from_attributes=True)`, `Field(...)`) for all request/response payloads and environment settings. Never pass raw unvalidated `dict` payloads into `service.py`.
4. **Thin Routers, Pure Services:** `router.py` only handles HTTP status codes, auth dependency injection (`Depends(get_current_user)`), and calling `service.py`. All business rules and DB transactions live in `service.py`.
5. **Async Safety & SQL Parameterization:** Never run blocking I/O (`time.sleep`, sync `requests`) inside `async def` endpoints (use `httpx.AsyncClient` or `def` threadpool routes). Always use parameterized SQLAlchemy / Supabase queries (never f-string SQL).

---

## 3. Pre-Commit & Hard-Failure Checklist (Verify Before Marking `[x]`)

- [ ] `uv run ruff check .` passes with zero lint/syntax errors
- [ ] `uv run pytest` passes for all unit/invariant tests in `tests/`
- [ ] All functions and endpoints have complete type annotations and Pydantic v2 `response_model`
- [ ] No cross-module internal imports (`app/modules/[a]/` importing `app/modules/[b]/` internals)
- [ ] No raw f-string SQL queries or hardcoded secrets/API keys
- [ ] All `AGENTS.md` Critical Constraints satisfied

---

# 🏗️ Stack Rules: Next.js + React + Supabase (`nextjs-supabase`)

---

## 1. Folder Responsibilities & Layer Boundaries (Pragmatic FDA)

This stack uses **Pragmatic Feature-Driven Architecture (FDA)** — domain logic grouped by isolated feature slice (`src/features/[domain]/`) so parallel developers and AI subagents never collide, pages as thin wrappers, and `src/lib/` as pure server/utility plumbing.

### Folder Map

| Folder | What Lives Here | What NEVER Lives Here |
|--------|-----------------|-----------------------|
| `src/app/` *(or `src/routes/` in Vite)* | Routes, thin `page.tsx` wrappers, `loading.tsx`, Route Handlers (`api/**/route.ts`) | Business logic, custom hooks, stateful UI components |
| `src/features/[domain]/` | Domain components, hooks, schemas/types, co-located tests (`__tests__/*.test.ts`) | Generic reusable UI, Supabase server clients, direct AI SDK calls in client components |
| `src/lib/` | Supabase clients (`@supabase/ssr`), AI client & `ai/prompts/`, server utilities, constants, utility tests (`__tests__/*.test.ts`) | JSX, React components, React hooks |
| `src/shared/ui/` | Generic stateless UI (`Button`, `Input`, `Modal`) used by 2+ features | Data fetching, Supabase calls, domain-specific logic |
| `src/shared/types/` | Database-generated types, global API/shared interfaces | Runtime business logic |
| `e2e/` | Playwright Golden-Path E2E specs (`e2e/<feature-slug>.spec.ts`) using `getByRole` / `getByLabel` | Brittle CSS-class selectors, unit tests (unit tests belong in `src/features/[domain]/__tests__/`) |

### Strict Import Matrix

| From Layer | Allowed to Import | Forbidden to Import |
|------------|-------------------|---------------------|
| `src/app/**/page.tsx` | **ONE** feature container from `src/features/[domain]/` | Multiple features, `src/lib/` business logic, stateful hooks |
| `src/features/[domain-a]/` | `src/shared/**`, `src/lib/utils/**`, own feature files | `src/features/[domain-b]/**` (peer features), `server-only` modules in Client Components |
| `src/shared/ui/` | External UI helpers (`clsx`, `lucide-react`) | `src/features/**`, Supabase clients, AI SDK |
| `src/lib/` | Server packages, `src/shared/types/` | JSX, React components, Client Components |
| `src/app/api/**/route.ts` | `src/lib/**`, `src/features/[domain]/schemas`, `src/shared/types/`, `zod` | Client Components, `src/features/**` UI |

---

## 2. Mandatory 2026 Next.js 15+, Supabase & AI SDK Rules

> **Code Templates:** See `.agents/skills/build/examples/` (`route-handler.ts.template`, `supabase-server.ts.template`, `ai-client.ts.template`, `rls-policies.sql.template`, `feature.test.ts.template`).

1. **Next.js 15+ Async Request APIs:** `params`, `searchParams`, `cookies()`, and `headers()` are **asynchronous Promises** — always `await params`, `await searchParams`, and `await cookies()`.
2. **Supabase `@supabase/ssr` Only:** Never install or import deprecated `@supabase/auth-helpers-nextjs`. On the server, always verify auth via `await supabase.auth.getUser()` (never trust `getSession()` on the server).
3. **Row-Level Security (RLS) Everywhere:** Every Supabase table must have RLS enabled with explicit policies (`USING (false)` for server-only tables). `SUPABASE_SERVICE_ROLE_KEY` must never appear in `NEXT_PUBLIC_*` or client code; every admin/service-role file must start with `import 'server-only'`.
4. **Server-Only AI SDK v4+ (`generateObject` / `streamText`):** All AI calls happen on the server (`import 'server-only'`) with prompt templates stored in `src/lib/ai/prompts/`. Use `generateObject` (or `Output.object`) with a Zod schema for structured JSON extraction instead of manual regex/JSON string parsing.
5. **Strict TypeScript & Component Limits:** `"strict": true`, zero `any` types (use `unknown` + Zod `safeParse`), React Server Components by default (`'use client'` only at interactive leaf components), and keep components **under 150 lines**.

---

## 3. Pre-Commit & Hard-Failure Checklist (Verify Before Marking `[x]`)

- [ ] `pnpm tsc --noEmit` passes with zero errors
- [ ] `pnpm test --run` passes for all unit/invariant tests in `src/features/[domain]/__tests__/`
- [ ] No `features/[a]/` importing from `features/[b]/`
- [ ] No business logic or hooks inside `src/app/**/page.tsx`
- [ ] `params`, `searchParams`, and `cookies()` are properly `await`ed (Next.js 15+)
- [ ] `import 'server-only'` at the top of every file using `SUPABASE_SERVICE_ROLE_KEY` or AI SDK
- [ ] Every Route Handler / Server Action validates input with `zod` (`safeParse`) and checks auth via `supabase.auth.getUser()`
- [ ] All AI prompts live in `src/lib/ai/prompts/` and have a corresponding AI eval test in `src/lib/ai/__tests__/*.eval.test.ts`
- [ ] No `any` types, no hardcoded hex colors where design tokens exist, and no `console.log` statements
- [ ] All new Supabase tables have RLS enabled and match `AGENTS.md` Critical Constraints
