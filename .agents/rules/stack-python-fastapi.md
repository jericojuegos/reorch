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
