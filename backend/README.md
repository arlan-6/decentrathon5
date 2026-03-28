# Minimal FastAPI CRUD + JWT Auth (Modular Folders)

This project provides a simple CRUD API for `items` using FastAPI + SQLAlchemy + PostgreSQL, with JWT authentication.

- API runs locally from Python
- Database runs in Docker (`postgres` only)
- Code is separated into folders: `api`, `core`, `models`, `schemas`, `repositories`, `services`

## Project Structure

```text
backend/
  main.py
  docker-compose.yml
  requirements.txt
  requirements.postgres.txt
  README.md
  .env.example
  api/
    deps.py
    v1/
      router.py
      endpoints/
        auth.py
        items.py
  core/
    config.py
    database.py
    security.py
  models/
    item.py
    user.py
  schemas/
    auth.py
    item.py
  repositories/
    item_repository.py
    user_repository.py
  services/
    auth_service.py
    item_service.py
  integrations/          # empty (reserved)
    llm/                 # empty (reserved)
  utils/                 # empty (reserved)
```

## Folder Usage

- `main.py`: app entrypoint, lifespan startup, root route
- `api/`: HTTP layer (routes + DI wiring)
- `core/`: database/config setup
- `models/`: SQLAlchemy models
- `schemas/`: Pydantic request/response models
- `repositories/`: DB access/query logic
- `services/`: business logic layer
- `integrations/`: future external integrations
- `utils/`: future shared helpers

## Run Database (Docker only)

```powershell
docker compose up -d postgres
```

PostgreSQL host mapping: `localhost:55432`.

## Run API Locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

API base: `http://127.0.0.1:8000`

## Environment Variable

Optional:

- `DATABASE_URL` (default: `postgresql+psycopg2://postgres:postgres@localhost:55432/decentrathon`)
- `JWT_SECRET` (set this in real environments)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `60`)

## Endpoints

- `GET /`
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me` (protected)
- `POST /items`
- `GET /items`
- `GET /items/{item_id}`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`

All `/items` endpoints are protected and require a Bearer token.

## Auth Flow

1. Register user via `POST /auth/register` (JSON body).
2. Login via `POST /auth/login` (form-data, OAuth2 style).
3. Use returned `access_token` as `Authorization: Bearer <token>`.
4. Call protected endpoints like `/auth/me` and `/items`.

## Example Requests

Register (JSON):

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"alice@example.com\",\"password\":\"StrongPass123!\",\"full_name\":\"Alice\",\"role\":\"candidate\"}"
```

Login (form-data):

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=StrongPass123!"
```

Get current user (protected):

```bash
curl "http://127.0.0.1:8000/auth/me" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Create item (protected):

```bash
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "{\"name\":\"first item\"}"
```

List items (protected):

```bash
curl "http://127.0.0.1:8000/items" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## How To Make Protected Endpoints

Use `get_current_user` dependency from `api.deps`.

Protect a whole router:

```python
from fastapi import APIRouter, Depends
from api.deps import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])
```

Protect a single endpoint:

```python
from fastapi import Depends
from api.deps import get_current_user
from models.user import User

@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
```

## API Docs

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Tip: In Swagger, click **Authorize**, paste `Bearer <ACCESS_TOKEN>`, and call protected routes.
