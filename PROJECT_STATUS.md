# Project Status — Cybersecurity Trainer Task Manager

## Specification Compliance & Session-Gated Progress
**Architecture Plan**: 25 Planned Development Sessions (Section 32)  
**Current Milestone**: Session 7 Complete — Ready for Session 8  
**Date**: 2026-09-20  
**Test Suite**: 104 Passed (0 Failures)  
**Frontend**: TypeScript 0 errors, Vite build successful  

---

## Master 25-Session Development Plan

| Session | Scope | Status | Notes |
| :---: | :--- | :---: | :--- |
| **1** | **Project foundation** | ✅ Done | Repository structure, FastAPI + Vite/React skeletons, Docker Compose, health endpoints, CI |
| **2** | **Database foundation** | ✅ Done | PostgreSQL async engine, base ORM model, Alembic migrations, health check |
| **3** | **Authentication** | ✅ Done | User model, bcrypt hashing, JWT auth, registration, login, auth middleware & tests |
| **4** | **Curriculum data model** | ✅ Done | Phase, SkillLayer, Domain, Topic, LearningObjective hierarchy with eager relationships |
| **5** | **Task engine & dependencies** | ✅ Done | Tasks, Subtasks, TaskPriority, TaskType, due dates, TaskDependency model & enforcement |
| **6** | **Full curriculum seed** | ✅ Done | Complete 196-day roadmap across all 28 weeks, 4 phases, 10 skill layers, 588 objectives |
| **7** | **Today view** | ✅ Done | Actionable daily view, daily objective banner, overdue queue, reflection & task detail modal |
| **8** | **Roadmap UI** | ⏳ **NEXT** | Full interactive roadmap navigation, phase/domain filters, progress indicators |

| **9** | **Study sessions** | 📋 Backlog | Timer engine (start/stop), session persistence, interruption tracking, actual study time |
| **10** | **Competency engine** | 📋 Backlog | 6 competency levels (Unknown → Teaching-ready), progression rules, mastery tracking |
| **11** | **Review engine** | 📋 Backlog | Spaced repetition, weak-area detection, confidence-based revision queue |
| **12** | **Evidence system** | 📋 Backlog | Practical work evidence attachments (screenshots, terminal logs, pcaps, writeups) |
| **13** | **Dashboard** | 📋 Backlog | 6 dedicated panels: Today, Progress, Practical, Teaching, Review, Portfolio |
| **14** | **Calendar** | 📋 Backlog | Day/Week/Month calendar views, drag-and-drop rescheduling without history corruption |
| **15** | **Projects and labs** | 📋 Backlog | Dedicated tracking for CTFs, isolated labs, security assessments, and completion evidence |
| **16** | **Teaching portfolio** | 📋 Backlog | Teaching as a 1st-class skill (explanations, lab manuals, quizzes, video recordings) |
| **17** | **Analytics** | 📋 Backlog | Velocity, completion rates, study-time tracking, competency trends, revision backlog |
| **18** | **Google integration foundation** | 📋 Backlog | Integration model, `SpreadsheetProvider` abstraction, secure credentials handling |
| **19** | **Google Sheets sync** | 📋 Backlog | Real-time mirror of Dashboard, Tasks, Competencies, and Portfolio sheets |
| **20** | **Sync reliability** | 📋 Backlog | Idempotent sync, retry queue, exponential backoff, conflict handling, sync status UI |
| **21** | **Import/export and backup** | 📋 Backlog | JSON/CSV export, curriculum import, disaster recovery backup/restore workflow |
| **22** | **Security hardening** | 📋 Backlog | Rate limiting, security headers, CSRF protection, audit logging, input sanitization |
| **23** | **End-to-end testing** | 📋 Backlog | Full user journey E2E tests, failure injection, sync failure recovery tests |
| **24** | **Deployment** | 📋 Backlog | Production Docker & Cloud configuration, migrations runner, zero-downtime deploy |
| **25** | **Final production readiness**| 📋 Backlog | Security audit, sync verification, disaster recovery drills, documentation signoff |

## Completed in Session 7: Today View

- **Frontend Today Execution Interface (`Today.tsx`)**:
  - **Daily Objective Banner**: Displays Day number, headline learning objective, domain hierarchy, and day-switcher input.
  - **Summary Metrics Bar**: Real-time progress bar, completion percentage, active vs completed counts, estimated vs logged study hours, and overdue counter.
  - **Overdue Revision Queue**: Dedicated alert card highlighting prior unfinished tasks with one-click completion.
  - **Actionable Task Cards**: Full status toggling (Todo, In Progress, Completed), type badges, priority indicators, estimated hours, and interactive subtask checkpoints.
  - **Task Detail & Reflection Modal (Section 22 UX)**:
    - Displays learning objective, action steps, deliverable/evidence criteria.
    - Learner reflection textarea: *"What did I understand today that I could not explain yesterday?"*
    - Interactive confidence score slider (0–100%) and actual hours logged input.
    - Full synchronization with the backend via `PATCH /api/v1/tasks/{id}`.
- **Backend API Additions**:
  - `GET /api/v1/tasks/today`: returns today's tasks with full attributes and subtasks.
  - `GET /api/v1/tasks/overdue`: returns uncompleted tasks assigned before today.
  - `GET /api/v1/tasks/summary/today`: returns aggregated progress percentages and headline daily objective.
  - `GET /api/v1/tasks/{task_id}`: returns task detail with topic, objectives, and prerequisites.
- **Navigation & Routing**:
  - Added `/today` route in `App.tsx` and linked "Today" in `Sidebar.tsx`.
- **Automated Tests**:
  - Added tests for `GET /tasks/overdue`, `GET /tasks/summary/today`, `GET /tasks/{id}`, and task completion workflow with confidence score and hours (104 backend tests total passing).

---

## Completed in Session 6: Full Curriculum Seed (196 Days)


- **Complete 196-Day Master Curriculum**:
  - Authored full dataset across all 28 weeks, 4 Phases, and 10 Skill Layers matching Section 8 specifications.
  - Every day contains structured, actionable learning objectives (588 total objectives) adhering to Section 7 guidelines (concepts to study, practical exercise, deliverable, self-assessment).
- **Seed Files & Formats**:
  - `backend/app/db/seeds/curriculum_data.json` (229 KB) — Full hierarchical JSON for database seeder.
  - `curriculum/roadmap.json` (229 KB) — Roadmap hierarchy for client/system consumers.
  - `curriculum/daily_tasks.json` (132 KB) — Flat daily task index for daily plan lookup.
  - `backend/scripts/generate_full_curriculum.py` — Deterministic generator script.
- **Automated Verification**:
  - Verified 196 unique, sequential days (Days 1 to 196) with zero gaps or duplicates.
  - Added 4 test suites in `backend/tests/test_seeder.py` verifying counts, sequential ordering, phases, and measurable objective descriptions.
  - Total backend tests: **100 passed** (0 failures).

---

## Completed in Session 5: Task Engine & Dependencies


- **Task Models & Enums**:
  - `TaskPriority`: `low`, `medium`, `high`, `critical`
  - `TaskType`: `study`, `practice`, `lab`, `ctf`, `reading`, `quiz`, `review`, `explain`, `teach`, `project`, `assessment`, `troubleshooting`
  - `TaskStatus`: `todo`, `in_progress`, `completed`, `blocked`, `skipped`, `needs_review`
  - Added `priority`, `task_type`, `due_date`, `confidence_score`, `review_date` to `Task` model.
- **Task Dependencies**:
  - Implemented `TaskDependency` ORM model (`task_id` -> `prerequisite_task_id`).
  - Added dependency enforcement in repository layer: blocks marking a task as `COMPLETED` if prerequisites are incomplete (unless `override_dependencies=True`).
- **Database Migrations**:
  - Generated and verified Alembic migration `d5e6f7g8h9i0_add_task_dependencies_and_fields.py`.
- **API Endpoints**:
  - `POST /api/v1/tasks/{id}/dependencies` — Add a prerequisite dependency.
  - `GET /api/v1/tasks/{id}/dependencies` — List dependencies for a task.
  - `DELETE /api/v1/tasks/{id}/dependencies/{prereq_id}` — Remove dependency.
  - `PATCH /api/v1/tasks/{id}` — Updated with dependency validation & `override_dependencies` support.
- **Automated Tests**:
  - Added comprehensive test suite for `TaskPriority`, `TaskType`, `TaskDependency`, blocked completion, override bypass, and dependency management routes.
  - 96 backend unit and integration tests passing.

---

## Current API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/v1/health` | — | Liveness probe |
| `GET` | `/api/v1/health/readiness` | — | Readiness probe (checks DB) |
| `POST` | `/api/v1/auth/register` | — | Create account |
| `POST` | `/api/v1/auth/login` | — | Get JWT token |
| `GET` | `/api/v1/auth/me` | 🔒 | Current user profile |
| `GET` | `/api/v1/curriculum/stats` | — | Aggregate curriculum statistics |
| `GET` | `/api/v1/curriculum/phases` | — | List all phases |
| `GET` | `/api/v1/curriculum/phases/{id}` | — | Phase with skill layers |
| `GET` | `/api/v1/curriculum/phases/{id}/full` | — | Phase full hierarchy |
| `GET` | `/api/v1/curriculum/skill-layers/{id}` | — | Skill layer with domains |
| `GET` | `/api/v1/curriculum/domains/{id}` | — | Domain with topics |
| `GET` | `/api/v1/curriculum/topics/{id}` | — | Topic with objectives |
| `GET` | `/api/v1/curriculum/day/{day_number}` | — | Topics for a specific day |
| `POST` | `/api/v1/tasks/generate` | 🔒 | Generate tasks for a curriculum day |
| `GET` | `/api/v1/tasks/today` | 🔒 | Get today's tasks |
| `PATCH` | `/api/v1/tasks/{id}` | 🔒 | Update task status, priority, type, notes |
| `POST` | `/api/v1/tasks/{id}/dependencies` | 🔒 | Add prerequisite dependency |
| `GET` | `/api/v1/tasks/{id}/dependencies` | 🔒 | List prerequisite dependencies |
| `DELETE` | `/api/v1/tasks/{id}/dependencies/{prereq_id}` | 🔒 | Remove prerequisite dependency |
| `PATCH` | `/api/v1/tasks/subtasks/{id}` | 🔒 | Update subtask status/notes |

---

## How to Run Current Version Locally

### Backend
```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`

### Frontend
```powershell
cd frontend
npm run dev
```
- Web UI: `http://localhost:5173`

---

## Next Session Objective
**Session 8 — Roadmap UI**:
- Build dedicated full-roadmap exploration page with Phase, Skill Layer, and Domain hierarchy navigation.
- Implement progress indicators, completed task counts, and visual mastery bars per domain.
- Add filtering by difficulty, phase, and completion status.


