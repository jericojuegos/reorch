# 🧠 Project Context & Antigravity Protocol

**Status:** Active  
**Source of Truth:** `.agent/` directory

## 1. Project Overview
**REORCH** is an AI-assisted audio re-orchestration platform designed to transform songs into new genres while preserving musical identity.

This project uses an AI-First development approach.

## 2. The "Brain" Structure (Directory Map)
All context is strictly organized. Do not search outside these folders for definitions.

- **📍 planning/** (`.agent/planning/`)
  - *Context:* Roadmap, Active Sprints, and Backlog.
  - *Key Files:* `00-roadmap.md`, `01-active-sprint.md`, `02-backlog.md`, `specify.md`.
  - *Usage:* Check this at the start of every session to align with priorities.

- **📂 knowledge/** (`.agent/knowledge/`)
  - *Context:* Facts, architecture, and specifications.
  - *Key Files:* `architecture.md`, `tech-stack.md`.
  - *Usage:* Read this BEFORE proposing architectural changes.

- **⚖️ rules/** (`.agent/rules/`)
  - *Context:* Non-negotiable laws and constraints.
  - *Key Files:* `budget-guard.md`, `coding-standards.md`, `security-policy.md`.
  - *Usage:* Read this BEFORE writing a single line of code.

- **⚡ workflows/** (`.agent/workflows/`)
  - *Context:* Standard Operating Procedures (SOPs).
  - *Key Files:* `phase-migration.md`.
  - *Usage:* Follow these strict steps for complex tasks.

- **🛠 skills/** (`.agent/skills/`)
  - *Context:* Tools and Capabilities.
  - *Usage:* Check `INDEX.md` to see what tools/scripts are available.

## 3. Operational Protocol (The "Prime Directive")
All AI Agents (Cursor, Windsurf, Copilot, Claude.ai, or similar) must follow this loop:

1.  **DISCOVER**: Read this README to understand the scope.
2.  **ALIGN**: Check `planning/01-active-sprint.md` to see what needs to be done. Explicitly look for **AD-HOC TASK** overrides.
3.  **VALIDATE**: Check `rules/` to ensure compliance.
4.  **LEARN**: Check `knowledge/` to understand existing patterns.
5.  **PLAN**: If a workflow exists in `workflows/`, adopt it.
6.  **EXECUTE**: Write code that matches the project's style.

## 4. Quick Reference
- **Current Task:** See `.agent/planning/01-active-sprint.md`.
- **Tech Stack:** See `.agent/knowledge/tech-stack.md`.
- **Architecture:** See `.agent/knowledge/architecture.md`.
