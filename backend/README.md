# Minimal FastAPI CRUD (Modular Folders)

This project provides a simple CRUD API for `items` using FastAPI + SQLAlchemy + PostgreSQL.

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
        items.py
  core/
    config.py
    database.py
  models/
    item.py
  schemas/
    item.py
  repositories/
    item_repository.py
  services/
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

Optional `DATABASE_URL` (default):

`postgresql+psycopg2://postgres:postgres@localhost:55432/decentrathon`

## Endpoints

- `GET /`
- `POST /items`
- `GET /items`
- `GET /items/{item_id}`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`

## Example Requests

Create:

```bash
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"first item\"}"
```

List:

```bash
curl "http://127.0.0.1:8000/items"
```

Update:

```bash
curl -X PUT "http://127.0.0.1:8000/items/1" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"updated item\"}"
```

Delete:

```bash
curl -X DELETE "http://127.0.0.1:8000/items/1"
```

## API Docs

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
