# REORCH Coding Standards

> Consistent code style and conventions for all REORCH development.

---

## 🐍 Python (Backend + Worker)

### Formatter & Linter
```bash
# Required tools
pip install black ruff isort

# Format command
black . && isort . && ruff check --fix .
```

### Style Rules
| Rule | Example |
|------|---------|
| **Line Length** | 88 chars (Black default) |
| **Quotes** | Double quotes `"` |
| **Imports** | Sorted with isort (profile=black) |
| **Type Hints** | Required for all function signatures |
| **Docstrings** | Google style for public functions |

### Naming
| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` | `process_track()` |
| Classes | `PascalCase` | `AudioPipeline` |
| Constants | `UPPER_SNAKE` | `MAX_FILE_SIZE` |
| Private | `_prefix` | `_internal_helper()` |

---

## 📘 TypeScript (Frontend)

### Formatter & Linter
```bash
# Required tools
npm install -D eslint prettier eslint-config-prettier

# Format command
npx prettier --write . && npx eslint --fix .
```

### Style Rules
| Rule | Example |
|------|---------|
| **Semicolons** | Required |
| **Quotes** | Single quotes `'` |
| **Trailing Commas** | Always (ES5) |
| **Type Annotations** | Explicit for props/returns |

### Naming
| Element | Convention | Example |
|---------|------------|---------|
| Components | `PascalCase` | `JobProgress.tsx` |
| Hooks | `useCamelCase` | `useJobStatus()` |
| Utils | `camelCase` | `formatDuration()` |
| Constants | `UPPER_SNAKE` | `API_BASE_URL` |
| **Custom Components** | `PascalCase.tsx` | `UploadForm.tsx` |
| **Next.js Reserved Files** | `lowercase.tsx` | `page.tsx`, `layout.tsx`, `loading.tsx` |
| Utils/Lib files | `camelCase.ts` | `audioHelpers.ts` |

> ⚠️ **Next.js App Router Reserved Files:** These MUST be lowercase:  
> `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.tsx`, `template.tsx`, `default.tsx`

---

## 📁 File Organization

### Frontend (`apps/web/`)
```
src/
├── app/              # Next.js App Router pages
├── components/       # Reusable UI components
│   ├── ui/           # shadcn/ui primitives
│   └── features/     # Feature-specific components
├── hooks/            # Custom React hooks
├── lib/              # Utilities, API clients
└── styles/           # Global styles
```

### Backend (`apps/api/`)
```
src/
├── api/              # Route handlers
│   └── v1/           # Versioned endpoints
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
└── core/             # Config, deps, exceptions
```

---

## 📝 Commit Messages

Format: `type(scope): message`

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructure (no behavior change) |
| `docs` | Documentation only |
| `chore` | Build, deps, config |
| `test` | Adding/fixing tests |

Examples:
```
feat(api): add job creation endpoint
fix(worker): handle FFmpeg timeout gracefully
refactor(web): extract upload logic to hook
```

---

## ✅ Pre-Commit Checklist

- [ ] Code formatted (Black/Prettier)
- [ ] Linter passes (Ruff/ESLint)
- [ ] Type hints present (Python) / types correct (TS)
- [ ] No `console.log` or `print()` debug statements
- [ ] No TODO comments without issue reference
