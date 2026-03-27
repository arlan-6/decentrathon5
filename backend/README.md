# Decentrathon Backend Architecture (Initial)

This backend uses a modular monolith with a layered architecture:

`API -> Service -> Repository -> PostgreSQL`

The first MVP scope is focused on CRUD for `Candidate` and `Application`.

## Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker Compose

## Project Structure

```text
backend/
  api/
    v1/
      endpoints/
        candidates.py
        applications.py
        health.py
      router.py
    deps.py
  core/
    config.py
    database.py
    logging.py
  models/
    candidate.py
    application.py
  schemas/
    candidate.py
    application.py
  repositories/
    candidate_repository.py
    application_repository.py
  services/
    candidate_service.py
    application_service.py
  main.py
  Dockerfile
  docker-compose.yml
  requirements.txt
  requirements.postgres.txt
```

## Layer Responsibilities

- API layer: routes, request/response schemas, HTTP status codes
- Service layer: business logic and orchestration
- Repository layer: SQLAlchemy queries and persistence
- Database layer: PostgreSQL storage

## MVP Entities

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
- `status`
- `submitted_at`

## API Scope (v1)

Base prefix: `/api/v1`

- `GET /health`
- `POST /candidates/`
- `GET /candidates/`
- `GET /candidates/{candidate_id}`
- `PUT /candidates/{candidate_id}`
- `DELETE /candidates/{candidate_id}`
- `POST /applications/`
- `GET /applications/`
- `GET /applications/{application_id}`
- `PUT /applications/{application_id}`
- `DELETE /applications/{application_id}`

## Environment Variables

The app reads settings from environment variables:

- `APP_NAME` (default: `Decentrathon Backend`)
- `DEBUG` (default: `false`)
- `DATABASE_URL` (default: `postgresql+psycopg2://postgres:postgres@localhost:55432/decentrathon`)
- `SECRET_KEY` (reserved for auth modules)
- `TOKEN_TTL_MINUTES` (reserved for auth modules)

## Run with Docker Compose

```powershell
docker compose up --build
```

Services:

- `api`: FastAPI on `http://localhost:8000`
- `postgres`: PostgreSQL on host port `55432`

## Run Locally (without Docker API container)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements.postgres.txt
uvicorn main:app --reload
```

Default DB URL:

`postgresql+psycopg2://postgres:postgres@localhost:55432/decentrathon`

## API Docs UI

After startup:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Request and Response Examples

All endpoints are prefixed with `/api/v1`.

### Health

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### Create Candidate

```bash
curl -X POST "http://localhost:8000/api/v1/candidates/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alice Johnson",
    "email": "alice@example.com",
    "city": "Almaty"
  }'
```

Response (201/200):

```json
{
  "id": 1,
  "full_name": "Alice Johnson",
  "email": "alice@example.com",
  "city": "Almaty",
  "created_at": "2026-03-27T18:00:00.000000+00:00"
}
```

### List Candidates

```bash
curl -X GET "http://localhost:8000/api/v1/candidates/"
```

### Get Candidate

```bash
curl -X GET "http://localhost:8000/api/v1/candidates/1"
```

### Update Candidate

```bash
curl -X PUT "http://localhost:8000/api/v1/candidates/1" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Astana"
  }'
```

### Delete Candidate

```bash
curl -X DELETE "http://localhost:8000/api/v1/candidates/1"
```

### Create Application

```bash
curl -X POST "http://localhost:8000/api/v1/applications/" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "essay_text": "My long-form essay...",
    "motivation_text": "I want to join because..."
  }'
```

Response (201/200):

```json
{
  "id": 1,
  "candidate_id": 1,
  "essay_text": "My long-form essay...",
  "motivation_text": "I want to join because...",
  "status": "submitted",
  "submitted_at": "2026-03-27T18:01:00.000000+00:00"
}
```

### List Applications

```bash
curl -X GET "http://localhost:8000/api/v1/applications/"
```

### Get Application

```bash
curl -X GET "http://localhost:8000/api/v1/applications/1"
```

### Update Application

```bash
curl -X PUT "http://localhost:8000/api/v1/applications/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_review"
  }'
```

### Delete Application

```bash
curl -X DELETE "http://localhost:8000/api/v1/applications/1"
```

## Error Handling

Common HTTP responses:

- `400 Bad Request`: validation/business rule errors (for example duplicate candidate email)
- `404 Not Found`: requested candidate/application does not exist
- `422 Unprocessable Entity`: invalid request payload format

## Request Flow

Example (`POST /candidates/`):

1. API endpoint validates request payload with Pydantic schema.
2. Service applies business rules.
3. Repository executes SQLAlchemy persistence.
4. API returns serialized response schema.

## Notes

- Current table creation uses SQLAlchemy `create_all` at app startup.
- For production evolution, add Alembic migrations to version schema changes.

## Extension Path

AI scoring should be added later as a separate service module (for example `ScoringService`) without mixing AI logic into CRUD endpoints.
