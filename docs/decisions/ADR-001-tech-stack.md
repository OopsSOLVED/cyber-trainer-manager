# ADR-001: Technology Stack Selection

**Status**: Accepted  
**Date**: 2026-09-17  
**Decision Makers**: Project owner

## Context

The Cybersecurity Trainer Task Manager is a production learning-management and task-execution application. It needs to be maintainable, testable, and support a growing feature set over 25+ development sessions.

## Decision

### Backend: Python + FastAPI + SQLAlchemy + PostgreSQL

**Rationale:**
- FastAPI provides automatic OpenAPI documentation, request validation via Pydantic, and native async support
- SQLAlchemy 2.0 offers a mature ORM with async capabilities and strong migration support via Alembic
- PostgreSQL is production-grade with excellent JSON support for flexible task metadata
- Python ecosystem has strong libraries for all planned integrations (Google Sheets, Redis, etc.)

**Alternatives considered:**
- Django: More opinionated, heavier for an API-first application
- Node.js/Express: Would require separate validation, ORM, and migration tooling
- Go: Faster runtime but slower development velocity for a feature-rich application

### Frontend: React + TypeScript + Vite

**Rationale:**
- React has the largest ecosystem and community support
- TypeScript catches errors at compile time and improves API contract safety
- Vite provides fast hot-module replacement and modern build tooling
- Component architecture maps well to the application's many feature pages

**Alternatives considered:**
- Next.js: SSR is unnecessary for a private task manager
- Vue: Smaller ecosystem for complex enterprise-style UIs
- Angular: Higher learning curve, more framework lock-in

### Database: PostgreSQL 16

**Rationale:**
- Supports complex relational schemas (curriculum hierarchy, task dependencies)
- JSONB columns for flexible metadata without schema changes
- Strong ACID compliance for data integrity
- Mature tooling for backups, migrations, monitoring

### Cache/Queue: Redis 7

**Rationale:**
- Session caching for authentication tokens
- Background job queue for Google Sheets sync
- Rate limiting support
- Lightweight and well-supported

### Infrastructure: Docker + Docker Compose

**Rationale:**
- Reproducible development environment across machines
- Easy onboarding for new contributors
- Same container images can be used in production
- Service isolation (backend, frontend, database, cache)

## Consequences

- Team must have Python and TypeScript knowledge
- PostgreSQL requires operational knowledge for production deployment
- Docker adds complexity but ensures environment consistency
- All dependencies are pinned for reproducibility
