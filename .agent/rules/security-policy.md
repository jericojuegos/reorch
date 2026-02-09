# REORCH Security Policy

> Non-negotiable security rules for all REORCH development.

---

## 🔐 Authentication & Authorization

| Rule | Implementation |
|------|----------------|
| **Stateless Auth** | JWT tokens validated on each request |
| **Token Storage** | `httpOnly` cookies only (no localStorage) |
| **Session Expiry** | Access tokens: 15 min, Refresh: 7 days |
| **RBAC** | Role-based access (user, admin) — enforce at API layer |

---

## 🛡️ Input Validation

| Rule | Implementation |
|------|----------------|
| **Server-Side First** | Never trust client-side validation alone |
| **Schema Validation** | Use Pydantic (Python) / Zod (TS) for all inputs |
| **File Uploads** | Validate MIME type + magic bytes, not just extension |
| **Size Limits** | Max file: 100MB, Max duration: 10 min |

---

## 🗄️ Database Security

| Rule | Implementation |
|------|----------------|
| **No Raw SQL** | Use ORM (SQLAlchemy) with parameterized queries |
| **Migrations Only** | Schema changes via Alembic — no manual DDL |
| **Least Privilege** | DB user has only required permissions |
| **Connection Pooling** | Use connection pool with timeout limits |

---

## 🌐 API Security

| Rule | Implementation |
|------|----------------|
| **HTTPS Only** | Enforce TLS in production |
| **CORS** | Whitelist specific origins, no wildcards |
| **Rate Limiting** | Per-user limits (e.g., 10 uploads/hour) |
| **Error Handling** | Never expose stack traces in responses |

---

## 📁 Storage Security

| Rule | Implementation |
|------|----------------|
| **Signed URLs** | All S3 access via time-limited signed URLs |
| **No Direct Paths** | Never expose internal bucket paths to clients |
| **Retention Policy** | Auto-delete uploads after 30 days |
| **Encryption** | S3 server-side encryption (SSE-S3) |

---

## 🚫 Prohibited Actions

| ❌ Never | Reason |
|----------|--------|
| Store passwords in plain text | Use bcrypt/argon2 |
| Log sensitive data (tokens, passwords) | PII exposure risk |
| Commit secrets to git | Use `.env` + secrets manager |
| Trust file extensions alone | MIME spoofing attacks |
| Execute user-uploaded files | Remote code execution risk |
| Clone celebrity voices | Legal/ethical liability |

---

## ✅ Required Checks Before Merge

- [ ] All inputs validated with Pydantic/Zod
- [ ] No secrets in code or logs
- [ ] CORS configured correctly
- [ ] Rate limits tested
- [ ] Error responses sanitized
