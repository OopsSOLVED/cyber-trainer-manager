# Cybersecurity Trainer Task Manager

A production task-management and learning platform that turns the cybersecurity-trainer skill stack into a daily execution plan, tracks progress, and mirrors the live dashboard into Google Sheets.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy, Alembic, Pydantic |
| **Frontend** | React 19, TypeScript, Vite |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **Infrastructure** | Docker, Docker Compose |
| **CI** | GitHub Actions |

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [Python 3.12+](https://www.python.org/)
- [Node.js 20+](https://nodejs.org/)
- [Git](https://git-scm.com/)

### Option 1: Docker Compose (Recommended)

```bash
# Clone and enter the project
cd cyber-trainer-manager

# Create environment file
cp .env.example .env

# Start all services
docker-compose up --build
```

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Frontend**: http://localhost:5173
- **Health Check**: http://localhost:8000/api/v1/health

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Development Commands

### Backend

| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | Start dev server |
| `pytest tests/ -v` | Run tests |
| `ruff check app/ tests/` | Lint code |
| `ruff format app/ tests/` | Format code |

### Frontend

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npx tsc -b` | Type check |
| `npm run lint` | Lint code |

## Project Structure

```
cyber-trainer-manager/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/v1/          # API endpoints (versioned)
│   │   ├── core/            # Configuration & shared utilities
│   │   ├── models/          # SQLAlchemy models (Session 2+)
│   │   ├── schemas/         # Pydantic schemas (Session 2+)
│   │   ├── services/        # Business logic (Session 3+)
│   │   ├── repositories/    # Data access layer (Session 2+)
│   │   ├── integrations/    # External services (Session 18+)
│   │   └── main.py          # Application factory
│   ├── tests/               # Backend test suite
│   ├── requirements.txt     # Production dependencies
│   └── requirements-dev.txt # Development dependencies
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── features/        # Feature-specific modules
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API client & utilities
│   │   └── types/           # TypeScript type definitions
│   └── ...
├── curriculum/               # Curriculum data (Session 6)
├── docs/                     # Documentation
│   ├── architecture/        # Architecture diagrams
│   └── decisions/           # Architecture Decision Records
├── infra/                    # Infrastructure configs
├── scripts/                  # Utility scripts
├── .github/workflows/        # CI/CD pipelines
├── docker-compose.yml        # Local dev environment
├── .env.example              # Environment template
├── PROJECT_STATUS.md         # Session progress tracker
└── CHANGELOG.md              # Version history
```

## Development Methodology

This project is built incrementally across **25 planned development sessions**. Each session produces one coherent, tested, working increment. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current progress.

## API Endpoints

### Currently Available

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/health` | Liveness probe |
| `GET` | `/api/v1/health/readiness` | Readiness probe |

### Planned (Future Sessions)

| Prefix | Description | Session |
|--------|-------------|---------|
| `/api/v1/auth` | Authentication | 3 |
| `/api/v1/curriculum` | Curriculum hierarchy | 4 |
| `/api/v1/tasks` | Task management | 5 |
| `/api/v1/dashboard` | Dashboard data | 13 |
| `/api/v1/integrations/google` | Google Sheets sync | 18–20 |

## License

Private — All rights reserved.
