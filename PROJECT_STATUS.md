# Project Status

## Current Session: 5 — Task System ✅

**Date**: 2026-09-19  
**Version**: 0.5.0

---

## Completed Work

### Session 5 — Task System

| Component | Status | Notes |
|-----------|--------|-------|
| Task & Subtask models | ✅ Done | Links User to Topic/LearningObjective |
| Task status enum | ✅ Done | todo, in_progress, completed, blocked, skipped |
| Daily generation engine | ✅ Done | Generates tasks based on 196-day curriculum plan |
| CRUD endpoints | ✅ Done | Generate, get today's tasks, update task/subtask |
| Alembic migration | ✅ Done | Foreign keys and constraints |
| Tests | ✅ Done | 12 tests for models, schemas, endpoints |

### Session 4 — Curriculum Model

| Component | Status | Notes |
|-----------|--------|-------|
| Curriculum models | ✅ Done | Phase, SkillLayer, Domain, Topic, LearningObjective |
| Hierarchical relationships | ✅ Done | Cascade deletes, ordering, day mapping |
| Alembic migration | ✅ Done | Foreign keys, indexes |
| Repository queries | ✅ Done | Eager-loading for nested relationships |
| API Endpoints | ✅ Done | Stats, list phases, get by ID with nesting, day schedule |
| Pydantic schemas | ✅ Done | Brief/Detail/Full response models |
| Tests | ✅ Done | 25 tests for models, schemas, endpoints |

### Session 3 — Authentication

| Component | Status | Notes |
|-----------|--------|-------|
| User model | ✅ Done | email, hashed_password, is_active, is_superuser, display_name |
| Registration | ✅ Done | POST /api/v1/auth/register |
| Login | ✅ Done | POST /api/v1/auth/login → JWT token |
| Password hashing | ✅ Done | bcrypt |
| Tests | ✅ Done | 26 tests |

### Session 2 — Database Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| SQLAlchemy async engine | ✅ Done | Connection pooling |
| Base ORM model | ✅ Done | id, created_at, updated_at |
| Alembic setup | ✅ Done | Async env.py |
| Database health check | ✅ Done | Readiness probe checks DB connectivity |
| Tests | ✅ Done | 15 tests |

### Session 1 — Project Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| Repository structure | ✅ Done | Full directory tree |
| Backend + Frontend | ✅ Done | FastAPI + Vite/React/TS |
| Docker Compose | ✅ Done | 4 services |
| CI pipeline | ✅ Done | GitHub Actions |

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/v1/health | — | Liveness probe |
| GET | /api/v1/health/readiness | — | Readiness probe (checks DB) |
| POST | /api/v1/auth/register | — | Create account |
| POST | /api/v1/auth/login | — | Get JWT token |
| GET | /api/v1/auth/me | 🔒 | Current user profile |
| GET | /api/v1/curriculum/stats | — | Aggregate curriculum statistics |
| GET | /api/v1/curriculum/phases | — | List all phases |
| GET | /api/v1/curriculum/phases/{id} | — | Phase with skill layers |
| GET | /api/v1/curriculum/phases/{id}/full | — | Phase full hierarchy |
| GET | /api/v1/curriculum/skill-layers/{id} | — | Skill layer with domains |
| GET | /api/v1/curriculum/domains/{id} | — | Domain with topics |
| GET | /api/v1/curriculum/topics/{id} | — | Topic with objectives |
| GET | /api/v1/curriculum/day/{day_number} | — | Topics for a specific day |
| POST | /api/v1/tasks/generate | 🔒 | Generate tasks for a curriculum day |
| GET | /api/v1/tasks/today | 🔒 | Get today's tasks |
| PATCH | /api/v1/tasks/{id} | 🔒 | Update task status/notes |
| PATCH | /api/v1/tasks/subtasks/{id} | 🔒 | Update subtask status/notes |

---

## Next Session: Session 6 — Database Seeding

### Objective
- Python seeding script to populate the curriculum tables
- Seed JSON files containing the actual cybersecurity roadmap data
- Alembic `seeds` folder structure

### Acceptance Criteria
- Seeder successfully inserts 4 Phases, 13 SkillLayers, Domains, Topics, and Objectives
- Relationships are preserved correctly
- Seed operation is idempotent (can run multiple times safely)
- A command exists to run the seeders easily
