---
description: "Automates the transition between project phases: audits completed work, clears the active board, and populates tasks for the next sprint."
---

# 🔄 Workflow: Phase Migration

**Trigger:** When a major Roadmap Phase is completed and we are moving to the next one.

## 1. Audit & Close
1.  **Review `planning/01-active-sprint.md`:** Ensure all items in "Current Task" and "Upcoming Tasks" are `[x]`. If any are `[ ]`, move them to the "Blocked" section or the next Phase in `planning/00-roadmap.md`.
2.  **Update `planning/00-roadmap.md`:** Mark the current Phase header as `[x]` (completed).
3.  **Update Activity Log:** Add a completion entry to `planning/01-active-sprint.md`.

## 2. Archive (Optional)
1.  If `planning/01-active-sprint.md` is cluttered, move the completed tasks (including those in the **Ad-Hoc / Side Quests** section) to `planning/03-history.md` (create if missing).
2.  **Clear** the completed items from the "Current Task", "Upcoming Tasks", and "Ad-Hoc / Side Quests" sections.

## 3. Activate Next Phase
1.  **Read `planning/00-roadmap.md`:** Identify the next Phase.
2.  **Update Sprint Header:** Change the sprint name and objective in `planning/01-active-sprint.md`.
3.  **Populate Current Task:** Copy the first high-level item from the new Phase into "Current Task".
4.  **Populate Upcoming Tasks:** Copy remaining items into "Upcoming Tasks".
5.  **Explode Tasks:** Break down each high-level item into technical sub-tasks:
    - Frontend components needed
    - Backend APIs needed
    - Database changes needed
    - Tests to write

## 4. User Verification
- Stop and ask the user: *"I have prepared the task list for Phase [X]. Please review the breakdown before we start coding."*

---

## File Reference
| File | Purpose |
|------|---------|
| `planning/00-roadmap.md` | High-level phases |
| `planning/01-active-sprint.md` | Current focus |
| `planning/02-backlog.md` | Full task backlog |
| `planning/03-history.md` | Archived completed work |