---
description: "Automates the transition between project phases: audits completed work, archives to history, and populates tasks for the next sprint."
---

# 🔄 Workflow: Phase Migration

**Trigger:** When a major Roadmap Phase is completed and we are moving to the next one.

## 1. Audit & Close
1.  **Review `planning/01-active-sprint.md`:** Ensure all items in "Current Task" and "Upcoming Tasks" are `[x]`. If any are `[ ]`, move them to the "Blocked" section or the next Phase in `planning/00-roadmap.md`.
2.  **Update `planning/00-roadmap.md`:** Mark the current Phase header as `[x]` (completed) and all its sub-items as `[x]`. Mark the next Phase header as `[>]` (current focus).
3.  **Update Activity Log:** Add a completion entry to `planning/01-active-sprint.md`.

## 2. Archive to History
*This step is **required**, not optional. History is the detailed execution record.*

1.  **Append** the completed Phase to `planning/03-history.md` (create if missing).
2.  **Include these sections** for each archived Phase:
    - All completed tasks grouped by area (Backend, Frontend, Pipeline, etc.)
    - Specific guardrails, limits, and configurations implemented (with values)
    - Bug fixes discovered during testing
    - Ad-Hoc / Side Quests completed
    - Activity Log with timestamps
3.  **Clear** the completed items from `01-active-sprint.md` (they now live in history).

> **Key distinction:** The Roadmap (`00-roadmap.md`) tracks *what* was planned. History (`03-history.md`) tracks *what was actually built and when*, including bug fixes and ad-hoc work that never appeared in the roadmap.

## 3. Activate Next Phase
1.  **Read `planning/00-roadmap.md`:** Identify the next Phase.
2.  **Rewrite `planning/01-active-sprint.md`:** Change the sprint name, objective, and context link.
3.  **Populate Current Task:** Copy the first high-level item from the new Phase into "Current Task".
4.  **Populate Upcoming Tasks:** Copy remaining items into "Upcoming Tasks".
5.  **Explode Tasks:** Break down each high-level item into technical sub-tasks:
    - Frontend components needed
    - Backend APIs / endpoints needed
    - Database / model changes needed
    - Worker / pipeline changes needed
    - Tests to write

## 4. Commit & User Verification
1.  **Commit** all planning file changes: `git commit -m "chore(agent): phase migration - close Phase N, prepare Phase N+1"`
2.  **Stop and ask the user:** *"I have prepared the task list for Phase [X]. Please review the breakdown before we start coding."*

---

## File Reference
| File | Purpose |
|------|---------|
| `planning/00-roadmap.md` | High-level phases and vision (what we *plan* to build) |
| `planning/01-active-sprint.md` | Current sprint focus (what we're *doing now*) |
| `planning/02-backlog.md` | Full task backlog (overflow / future ideas) |
| `planning/03-history.md` | Detailed execution log (what we *actually built*, per phase) |