# Project Status

## Current Session: 2 — Database Foundation ✅

**Date**: 2026-09-19  
**Version**: 0.2.0

---

## Completed Work

### Session 2 — Database Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| SQLAlchemy async engine | ✅ Done | Connection pooling, pool_pre_ping |
| Async session factory | ✅ Done | FastAPI dependency injection |
| Base ORM model | ✅ Done | id, created_at, updated_at + naming conventions |
| Database lifecycle | ✅ Done | init_db / close_db in app lifespan |
| Database health check | ✅ Done | check_db_health() for readiness probe |
| Readiness endpoint | ✅ Done | Now checks DB connectivity |
| Alembic setup | ✅ Done | Async env.py, initial migration |
| Configuration | ✅ Done | DATABASE_URL, DATABASE_TEST_URL, database_url_sync |
| Tests | ✅ Done | 26 tests passing (15 DB + 11 health) |

### Session 1 — Project Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| Repository structure | ✅ Done | Full directory tree per spec |
| Backend skeleton | ✅ Done | FastAPI app factory, config, health endpoints |
| Frontend skeleton | ✅ Done | Vite + React + TypeScript, design system |
| Docker Compose | ✅ Done | 4 services: backend, frontend, PostgreSQL, Redis |
| Environment config | ✅ Done | `.env.example` with all variables |
| CI pipeline | ✅ Done | GitHub Actions: lint + test + build |
| Documentation | ✅ Done | README, CHANGELOG, architecture, ADR |
| Health endpoint | ✅ Done | Liveness + readiness probes |
| Tests | ✅ Done | 9 health endpoint tests passing |

---

## Current Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Frontend (React)                   │
│              Vite Dev Server :5173                    │
│         ┌─────────────────────────┐                  │
│         │  Health Status Page     │                   │
│         │  (polls /api/v1/health) │                   │
│         └──────────┬──────────────┘                  │
└────────────────────┼─────────────────────────────────┘
                     │ HTTP (via Vite proxy)
┌────────────────────┼─────────────────────────────────┐
│                    ▼                                  │
│              Backend (FastAPI)                         │
│            Uvicorn Server :8000                        │
│         ┌─────────────────────────┐                  │
│         │  /api/v1/health         │                   │
│         │  /api/v1/health/readiness│ ← DB health     │
│         └──────────┬──────────────┘                  │
│                    │                                  │
│         ┌──────────▼──────────────┐                  │
│         │  SQLAlchemy Async Engine │                  │
│         │  Session Factory        │                   │
│         │  Base Model (abstract)  │                   │
│         └──────────┬──────────────┘                  │
└────────────────────┼─────────────────────────────────┘
                     │ asyncpg
┌────────────────────┼─────────────────────────────────┐
│            PostgreSQL 16 :5432  ← connected           │
│            Redis 7 :6379 (future)                     │
│            Alembic migration tracking                 │
└──────────────────────────────────────────────────────┘
```

---

## Commands

### Start Everything (Docker)
```bash
cp .env.example .env
docker-compose up --build
```

### Start Backend (Local)
```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Run Migrations
```bash
cd backend
alembic upgrade head
```

### Run Tests
```bash
cd backend
pytest tests/ -v
```

---

## Known Issues

- Alembic `autogenerate` requires a live PostgreSQL connection. Use Docker or local PostgreSQL when generating new migrations.
- The initial migration is empty because the Base model is abstract (no concrete tables until Session 3).

---

## Next Session: Session 3 — Authentication

### Objective
- User model (email, hashed password, profile fields)
- Password hashing (bcrypt via passlib)
- Registration endpoint
- Login endpoint (JWT token)
- Logout / session handling
- Authentication middleware / dependency
- Protected endpoint tests

### Acceptance Criteria
- User can register with email/password
- User can login and receive a JWT token
- Protected endpoints reject unauthenticated requests
- Password is hashed, never stored in plaintext
- All tests pass
