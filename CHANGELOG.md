# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.14.0] — 2026-09-20

### Added — Session 7: Today View & Actionable Daily Execution
- **Frontend Today Execution Interface (`frontend/src/pages/Today.tsx`)**:
  - **Daily Objective Banner**: Displays Day number, headline learning objective, domain context, and day-switcher input to jump between days.
  - **Summary Metrics Bar**: Real-time progress bar, completion percentage, active vs completed counts, estimated vs logged study hours, and overdue counter.
  - **Overdue Revision Queue**: Dedicated alert panel highlighting prior unfinished tasks with 1-click completion.
  - **Actionable Task Cards**: Full status toggling (Todo, In Progress, Completed), type badges, priority indicators, estimated hours, and interactive subtask checkpoints.
  - **Task Detail & Reflection Modal (Section 22 UX)**:
    - Displays learning objective, action steps, deliverable/evidence criteria.
    - Learner reflection prompt: *"What did I understand today that I could not explain yesterday?"*
    - Interactive confidence score slider (0–100%) and actual hours logged input with real-time API sync.
- **Backend API Additions**:
  - `GET /api/v1/tasks/today`: returns today's tasks with full attributes and subtasks.
  - `GET /api/v1/tasks/overdue`: returns uncompleted tasks assigned before today.
  - `GET /api/v1/tasks/summary/today`: returns aggregated progress percentages and headline daily objective.
  - `GET /api/v1/tasks/{task_id}`: returns task detail with topic, objectives, and prerequisites.
  - Task completion workflow in `task.py` repository supporting `confidence_score` and `actual_hours` updates.
- **Navigation & Routing**:
  - Registered `/today` route in `App.tsx` and added "Today" item with calendar icon to `Sidebar.tsx`.
- **Tests**:
  - Added 4 backend tests covering `/today/summary`, `/overdue`, task detail, and completion workflows with confidence/hours. Total 104 backend tests passing.

---

## [0.13.0] — 2026-09-20

### Added — Session 6: Full Curriculum Seed (196 Days)
- **Master Curriculum Dataset**:
  - Implemented the complete 196-day, 28-week curriculum mapped across 4 Phases, 10 Skill Layers, and 28 Domains directly matching Section 8 specifications.
  - Generated 588 measurable, actionable learning objectives spanning computer foundations, networking, Linux, Windows, offensive security, web applications, Active Directory/Kerberos, SOC/SIEM, malware analysis, reverse engineering, and trainer portfolio development.
- **Data Seed Files**:
  - `backend/app/db/seeds/curriculum_data.json` — Hierarchical schema for database seeding (229 KB).
  - `curriculum/roadmap.json` — Complete roadmap hierarchy (229 KB).
  - `curriculum/daily_tasks.json` — Indexed list of all 196 days with objectives and difficulty ratings (132 KB).
  - `backend/scripts/generate_full_curriculum.py` — Deterministic seed generator.
- **Tests**:
  - Added 4 validation tests in `test_seeder.py` verifying exact 196 days, sequential ordering (1-196), phase composition, and objective completeness (100 backend tests total passing).

---

## [0.12.0] — 2026-09-20


### Added — Session 5: Task Engine & Dependencies Realignment
- **Models**:
  - `TaskPriority`: `low`, `medium`, `high`, `critical`.
  - `TaskType`: `study`, `practice`, `lab`, `ctf`, `reading`, `quiz`, `review`, `explain`, `teach`, `project`, `assessment`, `troubleshooting`.
  - Added `priority`, `task_type`, `due_date`, `confidence_score`, and `review_date` to `Task` model.
  - `TaskDependency` ORM model for declaring prerequisite task chains.
- **Dependency Enforcement**:
  - Enforced prerequisite dependency validation in `update_task`: prevents accidental completion if prerequisites are incomplete.
  - Added `override_dependencies` flag allowing user override when desired.
- **API Endpoints**:
  - `POST /api/v1/tasks/{id}/dependencies`: declare a prerequisite dependency.
  - `GET /api/v1/tasks/{id}/dependencies`: list prerequisite dependencies.
  - `DELETE /api/v1/tasks/{id}/dependencies/{prereq_id}`: remove a prerequisite dependency.
- **Database Migrations**:
  - Alembic revision `d5e6f7g8h9i0_add_task_dependencies_and_fields.py`.
- **Tests**:
  - 7 new test cases covering task priorities, types, dependencies, blocked updates, and dependency management routes (96 tests total passing).

---

## [0.11.0] — 2026-09-19


### Added — Session 11: Dashboard Overview & Polish

#### UI Components
- `Dashboard.tsx` — High-level command center mapping to the `/` route.
- **Curriculum Stats**: Fetches and visualizes aggregated statistics from `/api/v1/curriculum/stats` (Phases, Skill Layers, Domains, Topics, Total Days).
- **Today's Mission Status**: Fetches today's tasks and calculates a progress percentage with a dynamic neon progress bar. Previews the top 3 tasks directly on the dashboard.
- **Empty States**: Elegant handling of unassigned tasks with prompt to generate them.
- **Cyber Styling**: Final polish with `lucide-react` iconography, glassmorphism panels, greeting logic based on time of day, and aesthetic background watermarks.

---

## [0.10.0] — 2026-09-19

### Added — Session 10: Daily Task UI

#### UI Components
- `Tasks.tsx` — Interactive daily task manager mapping to the `/tasks` route.
- **Task Generation**: Form to select a day number and generate tasks via `POST /api/v1/tasks/generate`.
- **Status Toggling**: Real-time optimistic UI updates utilizing Axios `PATCH` requests to cycle through task and subtask statuses (`todo`, `in_progress`, `completed`).
- **Cyber Styling**: Striking visual feedback with neon strike-throughs for completed items, pulsing neon highlights for in-progress items, and distinct structural glassmorphism layouts separating Tasks from Subtasks.

#### Architecture
- `task.ts` — Frontend TypeScript interfaces (`Task`, `Subtask`, `TaskStatus`, `TaskGenerationRequest`) strictly matching the FastAPI schemas.
- Removed the `/tasks` placeholder in `App.tsx` and mapped it to the new `Tasks` component.

---

## [0.9.0] — 2026-09-19

### Added — Session 9: Curriculum View UI

#### UI Components
- `Curriculum.tsx` — An interactive, lazy-loading accordion view of the entire 196-day cybersecurity roadmap.
- Implemented node components (`SkillLayerNode`, `DomainNode`, `TopicNode`) that recursively lazy-load and display child elements.
- Styled with Tailwind CSS matching the cyber-aesthetic (neon green, purple, and blue tier coloring).
- Uses `lucide-react` icons (ChevronRight, ChevronDown, Target, Clock, Shield) to denote hierarchy, difficulty, and duration.

#### Architecture
- `curriculum.ts` — Frontend TypeScript interfaces (`Phase`, `SkillLayer`, `Domain`, `Topic`, `Objective`) mapping directly to the backend Pydantic models.
- Replaced the placeholder `/curriculum` route in `App.tsx` with the new Curriculum component.

---

## [0.8.0] — 2026-09-19

### Added — Session 8: Authentication UI & Integration

#### UI Components
- `Login.tsx` — Login page featuring responsive glassmorphism panels, error handling, and form submission via Axios.
- `Register.tsx` — Registration page with automatic login upon success.
- `grid-pattern.svg` — Custom subtle background pattern for auth pages.

#### Architecture
- `ProtectedRoute.tsx` — Wrapper component that checks token validity via `/api/v1/auth/me` on initial load, showing an "INITIALIZING" state, and redirecting unauthorized users to `/login`.
- Updated `Sidebar.tsx` and `Header.tsx` to read the logged-in user's profile from the Zustand `useAuthStore` and properly log them out via the `api.ts` interceptor and state clearing.

---

## [0.7.0] — 2026-09-19

### Added — Session 7: Frontend Project Scaffold

#### UI & Layout
- Configured Tailwind CSS v3 with a custom "Cyber" color palette (neon greens, deep darks, purples).
- Created `Sidebar.tsx` for main navigation with active state styling.
- Created `Header.tsx` with a search bar and notifications layout.
- Created `MainLayout.tsx` structure wrapping the React Router `<Outlet />`.
- Created a dummy `Dashboard.tsx` with a stunning cyber-aesthetic grid for stats and activity placeholders.

#### Architecture
- Configured `React Router` in `App.tsx` with baseline routes (`/`, `/curriculum`, `/tasks`, `/labs`, `/settings`).
- Created `api.ts` using `axios` with global JWT request interception and 401 response handling.
- Implemented `useAuthStore.ts` using `zustand` to manage user authentication state.

---

## [0.6.0] — 2026-09-19

### Added — Session 6: Database Seeding

#### Curriculum Seeder
- `curriculum_data.json` — Subset of the 196-day cybersecurity roadmap covering Phase 1 (Foundations) and Phase 2 (Security & Exploitation) structured by skill layers, domains, topics, and objectives.
- `seeder.py` — Database seeder logic using SQLAlchemy to idempotently parse and insert the curriculum hierarchy.
- `seed.py` — CLI execution script (`python -m scripts.seed`) to initialize DB connection pool and trigger seeding.

#### Tests
- 3 new tests in `test_seeder.py` verifying JSON parsing, table clearing, and idempotent insertion logic.
- Total tests: 89 passing tests.

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
