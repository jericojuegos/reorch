---
description: Context Health Check
---

# Context Health Check

This workflow analyzes the `.agent` directory to ensure all rules, planning documents, and knowledge items are consistent, up-to-date, and healthy. 

**When to run:** 
- At the start or end of a sprint.
- After taking a prolonged break from the codebase.
- Whenever AI agents start hallucinating, ignoring rules, or forgetting previous decisions.

## Steps

1. **Rule Consolidation Check:**
   - Read all files in `.agent/rules/`.
   - Identify if there are any contradictory rules (e.g., `task-rules.md` requiring actions that `budget-guard.md` strictly prohibits).
   - Check if rules are concise enough to easily fit in the prompt window.

2. **Planning Alignment Check:**
   - Read `.agent/planning/00-roadmap.md` and `.agent/planning/01-active-sprint.md`.
   - Ensure the active sprint items align strictly with the roadmap vision.
   - Verify that there are no completed tasks (`[x]`) languishing in the active sprint board that need to be migrated to `03-history.md` (via `/phase-migration`).

3. **Knowledge Base Verification:**
   - Scan `.agent/knowledge/` files (e.g., `architecture.md`, `tech-stack.md`).
   - Cross-reference with the actual project source code or `package.json` to ensure the documented tech stack matches the real dependencies.

4. **Context Health Report Generation:**
   - Compile findings into a structured markdown report.
   - Categorize issues by: `CRITICAL` (rule conflicts), `WARNING` (stale state/planning drift), and `INFO` (optimizations).
   - Propose actionable steps or explicitly ask the user for permission to resolve the conflicts (e.g., "Would you like me to align `01-active-sprint.md` by moving items to history?").