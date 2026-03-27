# Decentrathon Backend

FastAPI backend scaffold using a clean layered architecture:

- `api` for HTTP endpoints and dependencies
- `services` for business logic
- `repositories` for data access
- `models` and `schemas` for domain and API contracts
- `integrations/llm` for pluggable LLM clients
- `core` for config, security, logging, and DB session placeholder

The current implementation is intentionally lightweight and uses in-memory repositories (no persistent database yet).

## Project Structure

```text
backend/
  main.py
  api/
    deps.py
    v1/
      router.py
      endpoints/
        auth.py
        candidates.py
        applications.py
        scoring.py
        reviews.py
        health.py
  core/
    config.py
    security.py
    database.py
    logging.py
  models/
  schemas/
  repositories/
  services/
  integrations/
    llm/
      base.py
      gemini_client.py
      openrouter_client.py
      ollama_client.py
  utils/
```

## Quick Start

### 1. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install fastapi uvicorn pydantic email-validator
```

### 3. Run the API

```powershell
uvicorn main:app --reload
```

App will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Overview (v1)

Base prefix: `/api/v1`

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /candidates/`
- `GET /candidates/`
- `POST /applications/`
- `GET /applications/`
- `POST /scoring/`
- `GET /scoring/`
- `POST /reviews/`
- `GET /reviews/`

## Authentication

OAuth2 Bearer is used for protected endpoints.

1. Register user via `/api/v1/auth/register`
2. Login via `/api/v1/auth/login` to get `access_token`
3. Send header: `Authorization: Bearer <token>`

## Example Flow

### Register

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"reviewer@example.com\",\"password\":\"secret123\",\"role\":\"reviewer\"}"
```

### Login

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"reviewer@example.com\",\"password\":\"secret123\"}"
```

### Create Candidate (authorized)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/candidates/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d "{\"full_name\":\"Alice Johnson\",\"email\":\"alice@example.com\",\"skills\":[\"python\",\"solidity\"]}"
```

## Environment Variables

Optional settings from `core/config.py`:

- `APP_NAME` (default: `Decentrathon Backend`)
- `DEBUG` (`true` or `false`, default: `false`)
- `SECRET_KEY` (default: `change-me`)
- `TOKEN_TTL_MINUTES` (default: `60`)

## Notes

- Data is not persisted across restarts.
- `integrations/llm/*` currently contains stub scoring logic.
- `core/database.py` is a placeholder for future DB integration.
