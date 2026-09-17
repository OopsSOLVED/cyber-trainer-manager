# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
