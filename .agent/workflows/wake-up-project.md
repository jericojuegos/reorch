---
description: Reads the hibernation state and recent Git history to instantly restore developer context and propose the next immediate action.
---
# ☀️ Workflow: Wake Up Project (Context Restoration)

**Role:** Lead Project Manager & Technical Onboarder
**Goal:** Ingest the frozen state of the project, read the recent Git history, and provide the user with a highly concise "Morning Briefing" so they can resume coding immediately without confusion.

---

## 🛑 Pre-Flight Constraints
1. **No Guessing:** Base your briefing strictly on the `01-active-sprint.md` file and the Git log. Do not hallucinate tasks that are not written down.
2. **Brevity:** The user wants to code, not read a novel. Keep the briefing under 150 words.

---

## 🏃‍♂️ Execution Steps

### Step 1: Ingest the Project Memory
1. Open `.agent/planning/01-active-sprint.md`.
2. Locate and read the `## 🧊 HIBERNATION STATE` section at the top of the file.
3. Read the `## 🔄 Current Task` section to understand the broader sprint goal.

### Step 2: Verify the Codebase State (Git)
1. Run `git status` to see if there are any uncommitted changes or stashed files left over from the hibernation.
2. Run `git log -n 5 --oneline` to read the last 5 commits. This verifies if the last action was a "WIP" commit or a completed feature.

### Step 3: Deliver the Morning Briefing
Output a clean, highly readable briefing to the user in the chat using this exact format:

> ### ☀️ Welcome Back to [Project Name]
> **Time Asleep:** [Calculate rough time since the date in the Hibernation State]
> 
> **📍 Where we left off:** 
> [Summarize the Current State from the Hibernation block and the last Git commit]
>
> **🎯 Your Immediate Next Step:**
> [Repeat the "Wake Up" Task from the Hibernation block]

### Step 4: Clean Up & Call to Action
1. **Crucial:** Remove the `## 🧊 HIBERNATION STATE` block from `01-active-sprint.md` now that the project is awake. Save the file.
2. Ask the user: *"Shall I open the relevant files and begin executing the immediate next step?"*
