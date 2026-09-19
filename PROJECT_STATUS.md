# Project Status

## Current Session: 3 — Authentication ✅

**Date**: 2026-09-19  
**Version**: 0.3.0

---

## Completed Work

### Session 3 — Authentication

| Component | Status | Notes |
|-----------|--------|-------|
| User model | ✅ Done | email, hashed_password, is_active, is_superuser, display_name |
| User migration | ✅ Done | users table with unique email index |
| Registration | ✅ Done | POST /api/v1/auth/register |
| Login | ✅ Done | POST /api/v1/auth/login → JWT token |
| Profile endpoint | ✅ Done | GET /api/v1/auth/me (protected) |
| Password hashing | ✅ Done | bcrypt (direct, not passlib) |
| JWT tokens | ✅ Done | HS256, configurable expiration |
| Auth dependencies | ✅ Done | get_current_user, get_current_superuser |
| User repository | ✅ Done | Data access layer for User queries |
| Tests | ✅ Done | 52 total tests passing |

### Session 2 — Database Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| SQLAlchemy async engine | ✅ Done | Connection pooling, pool_pre_ping |
| Base ORM model | ✅ Done | id, created_at, updated_at + naming conventions |
| Alembic setup | ✅ Done | Async env.py, initial migration |
| Database health check | ✅ Done | Readiness probe checks DB connectivity |
| Tests | ✅ Done | 26 tests |

### Session 1 — Project Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| Repository structure | ✅ Done | Full directory tree per spec |
| Backend + Frontend | ✅ Done | FastAPI + Vite/React/TS |
| Docker Compose | ✅ Done | 4 services |
| CI pipeline | ✅ Done | GitHub Actions |
| Tests | ✅ Done | 11 tests |

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/v1/health | — | Liveness probe |
| GET | /api/v1/health/readiness | — | Readiness probe (checks DB) |
| POST | /api/v1/auth/register | — | Create account |
| POST | /api/v1/auth/login | — | Get JWT token |
| GET | /api/v1/auth/me | 🔒 | Current user profile |

---

## Next Session: Session 4 — Curriculum Model

### Objective
- Curriculum data model (Phase, SkillLayer, Domain, Topic, LearningObjective)
- Hierarchical relationships: Phase → SkillLayer → Domain → Topic → Objective
- CRUD endpoints for reading curriculum (admin write)
- Alembic migration for all curriculum tables
- Seed-ready schema (data loaded in Session 6)

### Acceptance Criteria
- All curriculum tables created via migration
- GET endpoints return curriculum hierarchy
- Tests pass for all curriculum endpoints
- Schema supports the 196-day learning plan structure
