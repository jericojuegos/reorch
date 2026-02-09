---
trigger: always_on
---

# 💰 Rule: Budget Guard & Token Efficiency

**Purpose:** Prevent token waste, runaway loops, and context bloat.

## 1. The "Pause & Ask" Protocol
You **MUST** pause execution and request user approval if **ANY** of the following thresholds are met:

- **File Scope:** You intend to edit more than **3 files** in a single turn (cumulative).
- **System Impact:** You intend to run more than **2 destructive/long-running commands** (e.g., installs, builds, migrations).
- *Exemption:* Read-only commands (`ls`, `cat`, `grep`, `pwd`) do not count.
- **Destructive Actions:** You intend to delete files, drop database tables, or overwrite configs.

*Trigger phrase:* "⚠️ **BUDGET GUARD TRIGGERED**: [Reason]. Awaiting approval..."

## 2. Loop Prevention (The "3-Strike Rule")
If you have attempted to fix the same error **3 times** without success:
1.  **STOP** immediately.
2.  Do **NOT** try a 4th time blindly.
3.  Report the specific error and ask for guidance.

## 3. Artifact Priority
- **Plan First:** For any multi-file change, generate a concise **Implementation Plan** (markdown list) first.
- **Code Second:** Wait for explicit user confirmation before generating full code.

## 4. Context Compression (TOON)
When displaying large data, use **TOON (Token-Oriented Object Notation)**:
- **Skip boilerplate:** Replace standard imports with `// ...`.
- **Focus on changes:** Only show lines relevant to the logic.
- **Abbreviate keys:** Use shorter keys in summaries.

#### TOON Example:
```javascript
// ❌ Verbose (~200 tokens)
{
  "user_identifier": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "email_address": "test.user@example.com",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-02-05T14:22:11Z"
}

// ✅ TOON (~50 tokens, 75% reduction)
{ id: "a1b2...", email: "test.u@...", ts: "2024-01..." /* +1 field */ }