# Architecture Overview

## System Architecture

The Cybersecurity Trainer Task Manager follows a clean layered architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ React + TypeScript (Vite)                              │ │
│  │  • Pages        — route-level components               │ │
│  │  • Components   — reusable UI elements                 │ │
│  │  • Features     — feature-specific modules             │ │
│  │  • Services     — API client layer                     │ │
│  │  • Hooks        — shared React hooks                   │ │
│  │  • Types        — TypeScript definitions               │ │
│  └───────────────────────┬────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │ REST API (JSON)
┌──────────────────────────┼──────────────────────────────────┐
│                     API LAYER                                │
│  ┌───────────────────────▼────────────────────────────────┐ │
│  │ FastAPI                                                │ │
│  │  • Versioned routes (/api/v1/...)                      │ │
│  │  • Request validation (Pydantic)                       │ │
│  │  • Authentication middleware (Session 3)                │ │
│  │  • CORS, security headers                              │ │
│  └───────────────────────┬────────────────────────────────┘ │
│  ┌───────────────────────▼────────────────────────────────┐ │
│  │ Service Layer                                          │ │
│  │  • Business logic                                      │ │
│  │  • Orchestration                                       │ │
│  │  • Domain rules                                        │ │
│  └───────────────────────┬────────────────────────────────┘ │
│  ┌───────────────────────▼────────────────────────────────┐ │
│  │ Repository Layer                                       │ │
│  │  • Data access                                         │ │
│  │  • SQLAlchemy queries                                  │ │
│  │  • Transaction management                              │ │
│  └───────────────────────┬────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                     DATA LAYER                               │
│  ┌───────────────────────▼──────┐  ┌──────────────────────┐ │
│  │ PostgreSQL 16                │  │ Redis 7              │ │
│  │  • Primary data store        │  │  • Session cache     │ │
│  │  • Migrations via Alembic    │  │  • Background jobs   │ │
│  └──────────────────────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                  INTEGRATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Provider Abstraction (SpreadsheetProvider)               ││
│  │  └── GoogleSheetsProvider                                ││
│  │       • Dashboard sheet                                  ││
│  │       • Daily tasks sheet                                ││
│  │       • Competency sheet                                 ││
│  │       • Portfolio sheet                                  ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

1. **Layered architecture** — API → Service → Repository → Database. Each layer has a single responsibility.
2. **Versioned API** — All endpoints are under `/api/v1/` to allow future breaking changes.
3. **Configuration via environment** — Pydantic Settings reads from `.env` / environment variables.
4. **Application factory** — `create_app()` function allows test configuration overrides.
5. **Provider abstraction** — External integrations (Google Sheets) use abstract interfaces for testability.
6. **Data-driven curriculum** — Curriculum is stored in the database, not hard-coded in the frontend.

## Component Status

| Component | Status | Session |
|-----------|--------|---------|
| Application skeleton | ✅ | 1 |
| Database | 🔲 Planned | 2 |
| Authentication | 🔲 Planned | 3 |
| Curriculum model | 🔲 Planned | 4 |
| Task engine | 🔲 Planned | 5 |
| Curriculum seed | 🔲 Planned | 6 |
| Today view | 🔲 Planned | 7 |
| Roadmap UI | 🔲 Planned | 8 |
| Study sessions | 🔲 Planned | 9 |
| Competency engine | 🔲 Planned | 10 |
| Review engine | 🔲 Planned | 11 |
| Evidence system | 🔲 Planned | 12 |
| Dashboard | 🔲 Planned | 13 |
| Calendar | 🔲 Planned | 14 |
| Projects & labs | 🔲 Planned | 15 |
| Teaching portfolio | 🔲 Planned | 16 |
| Analytics | 🔲 Planned | 17 |
| Google integration | 🔲 Planned | 18–20 |
| Import/export | 🔲 Planned | 21 |
| Security hardening | 🔲 Planned | 22 |
| E2E testing | 🔲 Planned | 23 |
| Deployment | 🔲 Planned | 24 |
| Production readiness | 🔲 Planned | 25 |
