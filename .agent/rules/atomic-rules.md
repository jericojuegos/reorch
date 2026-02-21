---
trigger: always_on
---

# ⚛️ Rule: Atomic Execution

**Purpose:** Prevent error cascades, protect API budget (token limits), and ensure code is "Green" (passing) before adding complexity.

## 1. The Standard Protocol
You must execute tasks in this strict, isolated loop:

1.  **READ:** Identify the *next* unchecked item in `01-active-sprint.md` (or the Ad-Hoc section if triggered).
2.  **ISOLATE:** Can this task run on its own without breaking the app?
    * *For Antigravity: a task is isolatable if it doesn't require an unregistered handler or unresolved service binding.*
    * **YES:** Proceed to step 3.
    * **NO:** Switch to Section 2 (Coupled Logic).
3.  **EXECUTE & VERIFY:** Implement the code and verify it works (no console errors, UI renders, or tests pass).
    * **If verification fails:** Do NOT proceed to Step 4. Treat as a failed atomic unit — rollback or stash changes, log the failure in the sprint board with a `[!]` marker, and pause for user input.
4.  **UPDATE TRACKER:** Immediately mark the task as `[x]` in `01-active-sprint.md`. DO NOT skip this step.
5.  **COMMIT:** `git commit -m "feat(scope): [task name]"` *(Use `fix:`, `chore:`, `refactor:`, or `docs:` if it was an Ad-Hoc tweak).*
6.  **REPEAT.**

## 2. Exception: Coupled Logic (The "Batch" Rule)
*Use this ONLY when tasks are physically dependent on each other.*

If Task A (e.g., API Route) imports Task B (e.g., Database Model), and the code cannot compile without both:
1.  **DECLARE IT:** Explicitly state in the chat: *"Task A and Task B are coupled dependencies. Executing as an Atomic Group to save context window and budget."*
2.  **BATCH EXECUTE:** Implement both files in the same turn.
3.  **JOINT VERIFY:** Verify them together.
4.  **SYNC & COMMIT:** Mark both as `[x]` in the sprint board, then commit them as one unit.

## ⛔ 3. STRICT PROHIBITIONS:
* **The "YAGNI" Rule:** Never batch tasks just to "save time." If it's not required for the current atomic step to compile, do not write it.
* **Context Bloat:** Never batch unrelated tasks (e.g., "Fixing the Header" and "Updating the Database"). This wastes API tokens and increases hallucination risk.

## 4. Recovery Protocol
After any hard stop (e.g., failed verify, budget guard triggered, or the 3-Strike rule):
1. Do NOT resume from memory. Re-read `01-active-sprint.md`.
2. Identify the last `[x]` item as your baseline.
3. The next unchecked item is your restart point.
4. Report your restart point to the user before proceeding.
