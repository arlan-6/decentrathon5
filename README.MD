# Decentrathon

Decentrathon is a full-stack application for managing candidate submissions and applications.

Current implementation status:
- Backend CRUD API for candidates and applications is working.
- Frontend is scaffolded and running with Vite + React + TypeScript.
- Auth, review, and AI scoring modules exist in the backend codebase but are not mounted on the active API router yet.

## Monorepo Structure

```text
decentrathon/
	backend/   # FastAPI + SQLAlchemy + PostgreSQL
	frontend/  # React + TypeScript + Vite + Tailwind + shadcn/ui
```

For subsystem-specific details:
- Backend docs: `backend/README.md`
- Frontend docs: `frontend/README.md`

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn
- Docker Compose (optional local orchestration)

### Frontend
- React 19
- TypeScript 5
- Vite 8
- React Router 7
- Tailwind CSS 4
- shadcn/ui primitives

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+
- Docker Desktop (optional, for containerized backend/postgres)

## Quick Start

### Option A: Run Backend with Docker + Frontend Locally

1. Start backend and database:

```powershell
cd backend
docker compose up --build
```

2. Start frontend:

```powershell
cd frontend
npm install
npm run dev
```

3. Open:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs

### Option B: Run Everything Locally (No Docker)

1. Start PostgreSQL manually and make sure it matches your `DATABASE_URL`.

2. Start backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements.postgres.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Start frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

## Backend Environment Variables

The backend reads settings from environment variables:

- `APP_NAME` (default: `Decentrathon Backend`)
- `DEBUG` (default: `false`)
- `DATABASE_URL` (default: `postgresql+psycopg2://postgres:postgres@localhost:55432/decentrathon`)
- `SECRET_KEY` (default: `change-me`)
- `TOKEN_TTL_MINUTES` (default: `60`)

When using `backend/docker-compose.yml`, the API container uses:
- `DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/decentrathon`

## Current API Surface (Mounted Routes)

Base prefix: `/api/v1`

- `GET /health`

Candidate endpoints:
- `POST /candidates/`
- `GET /candidates/`
- `GET /candidates/{candidate_id}`
- `PUT /candidates/{candidate_id}`
- `DELETE /candidates/{candidate_id}`

Application endpoints:
- `POST /applications/`
- `GET /applications/`
- `GET /applications/{application_id}`
- `PUT /applications/{application_id}`
- `DELETE /applications/{application_id}`

Also available:
- `GET /` (root health message)

## Data Model (MVP)

### Candidate
- `id`
- `full_name`
- `email`
- `city`
- `created_at`

### Application
- `id`
- `candidate_id`
- `essay_text`
- `motivation_text`
- `status` (default: `submitted`)
- `submitted_at`

## Notes on In-Progress Modules

The backend includes additional modules (`auth`, `reviews`, `scoring`, LLM integrations), but the active `api/v1/router.py` currently mounts only:
- health
- candidates
- applications

If you plan to enable auth/scoring routes, update router wiring and dependency providers accordingly.

## Useful Commands

### Backend

```powershell
cd backend
uvicorn main:app --reload
```

### Frontend

```powershell
cd frontend
npm run dev
npm run build
npm run lint
```

## Development Notes

- Database tables are created at backend startup via SQLAlchemy `create_all`.
- For production schema evolution, add Alembic migrations.
- Frontend route configuration is currently minimal and ready for expansion in `frontend/src/main.tsx` and `frontend/src/pages/`.