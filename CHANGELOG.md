# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.5.0] — 2026-09-19

### Added — Session 5: Task System

#### Task Models
- `Task` ORM model (Topic assigned to a User)
- `Subtask` ORM model (LearningObjective assigned to a User)
- `TaskStatus` Enum (`todo`, `in_progress`, `completed`, `blocked`, `skipped`)
- Time tracking fields (`estimated_hours`, `actual_hours`)
- Scheduling fields (`assigned_date`, `completed_at`)
- Alembic migration for task tables

#### Task Endpoints
- `POST /api/v1/tasks/generate` — Generate tasks for a specific curriculum day
- `GET /api/v1/tasks/today` — Get today's assigned tasks
- `PATCH /api/v1/tasks/{task_id}` — Update task status/notes
- `PATCH /api/v1/tasks/subtasks/{subtask_id}` — Update subtask status/notes

#### Architecture
- `models/task.py` — Task execution layer models
- `repositories/task.py` — Logic for task generation and retrieval
- `api/v1/tasks.py` — Task router (protected by authentication)
- `schemas/task.py` — Pydantic schemas for tasks and subtasks

#### Tests
- 12 new task tests (models, schemas, and endpoints)
- All 86 tests pass without requiring a live PostgreSQL instance

---

## [0.4.0] — 2026-09-19

### Added — Session 4: Curriculum Model

#### Curriculum Models
- `Phase` ORM model (top-level grouping)
- `SkillLayer` ORM model (major skill category, maps to the 13 roadmap items)
- `Domain` ORM model (sub-area within a skill layer)
- `Topic` ORM model (individual learning topic, mapped to a day in the 196-day plan)
- `LearningObjective` ORM model (specific measurable learning goal)
- Alembic migration for all curriculum tables with foreign keys and cascade deletes

#### Curriculum Endpoints
- `GET /api/v1/curriculum/phases` — List all phases
- `GET /api/v1/curriculum/phases/{phase_id}` — Get phase with skill layers
- `GET /api/v1/curriculum/phases/{phase_id}/full` — Get phase with full hierarchy
- `GET /api/v1/curriculum/skill-layers/{layer_id}` — Get skill layer with domains
- `GET /api/v1/curriculum/domains/{domain_id}` — Get domain with topics
- `GET /api/v1/curriculum/topics/{topic_id}` — Get topic with objectives
- `GET /api/v1/curriculum/day/{day_number}` — Get topics for a specific day
- `GET /api/v1/curriculum/stats` — Curriculum statistics

#### Architecture
- `models/curriculum.py` — Hierarchical ORM models
- `repositories/curriculum.py` — Data access layer with eager-loading queries
- `api/v1/curriculum.py` — Read-only curriculum router
- `schemas/curriculum.py` — Pydantic schemas with brief/detail/full nesting levels

#### Tests
- 25 new curriculum tests (models, schemas, and endpoints)
- All 74 tests pass without requiring a live PostgreSQL instance

---

## [0.3.0] — 2026-09-19

### Added — Session 3: Authentication

#### User Model
- `User` ORM model with email, hashed_password, is_active, is_superuser, display_name, last_login_at
- Alembic migration to create `users` table with unique email index

#### Authentication Endpoints
- `POST /api/v1/auth/register` — Create new user account (email validation, password >= 8 chars)
- `POST /api/v1/auth/login` — Authenticate and receive JWT access token
- `GET /api/v1/auth/me` — Get current user profile (protected)

#### Security
- Password hashing with bcrypt (direct, not via passlib — avoids bcrypt 5.x compat issues)
- JWT access tokens with HS256 signing (configurable expiration)
- OAuth2 Bearer token scheme
- Active/inactive account enforcement
- Superuser guard dependency for admin-only endpoints

#### Architecture
- `services/auth.py` — Password hashing + JWT creation/validation
- `repositories/user.py` — Data access layer for User queries
- `api/deps.py` — `get_current_user` and `get_current_superuser` FastAPI dependencies
- `schemas/auth.py` — Pydantic request/response models with email validation

#### Tests
- 26 new auth tests (password hashing, JWT tokens, registration, login, protected endpoints)
- All 52 tests pass without requiring a live PostgreSQL instance

---

## [0.2.0] — 2026-09-19

### Added — Session 2: Database Foundation

#### Database Infrastructure
- Async SQLAlchemy engine with connection pooling (`core/database.py`)
- Async session factory with FastAPI dependency injection (`get_db`)
- Base ORM model with id, created_at, updated_at columns (`models/base.py`)
- Consistent naming conventions for Alembic migrations
- Database lifecycle management (init_db, close_db) integrated into app lifespan
- Database health check function (`check_db_health`) for readiness probe

#### Alembic Migrations
- Alembic initialized with async env.py configuration
- `alembic.ini` configured with project database URL
- Initial migration revision (empty — Base is abstract)

#### Configuration
- `DATABASE_TEST_URL` setting for test isolation
- `database_url_sync` property for Alembic compatibility

#### Readiness Endpoint
- `/api/v1/health/readiness` now checks real database connectivity
- Reports "degraded" status when PostgreSQL is unreachable

#### Tests
- 15 new database tests (config, engine, Base model, health check, lifecycle, session)
- Updated health tests with mocked DB fixtures (healthy + degraded states)
- All 26 tests pass without requiring a live PostgreSQL instance

---

## [0.1.0] — 2026-09-17

### Added — Session 1: Project Foundation

#### Backend
- FastAPI application skeleton with application factory pattern
- Pydantic-based configuration system (reads from `.env`)
- Health check endpoint (`GET /api/v1/health`)
- Readiness probe endpoint (`GET /api/v1/health/readiness`)
- Structured logging with environment-aware log levels
- CORS middleware with configurable origins
- Backend Dockerfile (Python 3.12, non-root user, health check)
- Pytest test suite with 10 health endpoint tests
- Ruff linter and formatter configuration
- Package structure for future modules (models, schemas, services, repositories, integrations)

#### Frontend
- Vite + React 19 + TypeScript project
- Premium dark-mode design system with CSS custom properties
- Glassmorphism card components
- Micro-animations (fade-in, float, pulse)
- Inter + JetBrains Mono typography
- Live health status page with 30-second polling
- Typed API client (`services/api.ts`)
- Vite dev proxy to backend (avoids CORS in development)
- Frontend Dockerfile (Node 20 Alpine)

#### Infrastructure
- Docker Compose with four services (backend, frontend, PostgreSQL 16, Redis 7)
- Health checks on all infrastructure services
- Named volumes for data persistence
- Shared bridge network
- Environment template (`.env.example`)

#### CI/CD
- GitHub Actions workflow (`ci.yml`)
- Backend job: Ruff lint + format check + pytest
- Frontend job: TypeScript type check + build validation

#### Documentation
- `README.md` — Project overview, tech stack, quick start, commands, structure
- `PROJECT_STATUS.md` — Session tracking document
- `CHANGELOG.md` — Version history
- `docs/architecture/overview.md` — Architecture diagram and component descriptions
- `docs/decisions/ADR-001-tech-stack.md` — Technology choices and rationale
