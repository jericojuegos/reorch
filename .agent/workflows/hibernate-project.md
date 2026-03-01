---
description: Captures the current state, uncommitted changes, and immediate next steps before pausing development on a project.
---
# 🧊 Workflow: Hibernate Project (Cryo-Sleep)

**Role:** Lead Project Manager & Technical Scribe
**Goal:** Freeze the current state of the project, document broken code/blockers, and write a clear "Wake Up" briefing in the sprint board so development can resume flawlessly months later.

---

## 🛑 Pre-Flight Constraints
1. **No Code Changes:** Do not attempt to fix any bugs or write new feature code during this workflow. Your only job is documentation.
2. **Honesty:** If the code is currently broken or failing tests, you MUST state that clearly. Do not pretend the codebase is stable if it isn't.

---

## 🏃‍♂️ Execution Steps

### Step 1: Analyze Current Workspace State
1. Read the current `git status` and `git diff` (if applicable/accessible) to see what files were actively being modified.
2. Read the `## 🔄 Current Task` section in `.agent/planning/01-active-sprint.md` to understand what the user was trying to accomplish.

### Step 2: Draft the Hibernation Briefing
1. Open `.agent/planning/01-active-sprint.md`.
2. Insert a new section at the very top of the file called `## 🧊 HIBERNATION STATE`.
3. Fill out this exact template based on your analysis:
   ```markdown
   ## 🧊 HIBERNATION STATE (Initiated: [Current Date])
   * **Last Action Taken:** [Briefly describe the last file edited or command run]
   * **Current State:** [e.g., "The API route is returning a 500 error", or "The UI is built but not wired to Zustand"]
   * **The "Wake Up" Task:** [Explicitly state the very first thing the developer should do when they return. E.g., "Fix the asyncpg enum binding in worker.py"]
   ```
