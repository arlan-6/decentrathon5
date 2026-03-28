# Minimal FastAPI CRUD (Single File)

This project now has:

- one Python file: `main.py`
- one CRUD resource: `items`
- PostgreSQL in Docker Compose (DB only)
- legacy architecture folders kept as placeholders (not removed)

## Current Structure

```text
backend/
  main.py
  docker-compose.yml
  requirements.txt
  requirements.postgres.txt
  README.md
  test_main.http
  .env.example
  api/                  # empty placeholder
  core/                 # empty placeholder
  models/               # empty placeholder
  schemas/              # empty placeholder
  repositories/         # empty placeholder
  services/             # empty placeholder
  integrations/         # empty placeholder
  integrations/llm/     # empty placeholder
  utils/                # empty placeholder
```

## How to Use Folders

Right now, the API runs only from `main.py`. The placeholder folders are kept for future modularization.

- `main.py`: all running code (model, schemas, DB session, routes)
- `api/`: move route handlers here when splitting the app
- `core/`: shared config, DB bootstrap, logging utilities
- `models/`: SQLAlchemy ORM models (one file per entity)
- `schemas/`: Pydantic request/response models
- `repositories/`: DB query layer
- `services/`: business logic layer
- `integrations/`: external clients (LLM, email, webhooks, etc.)
- `utils/`: shared helpers/constants

Recommended migration path later:

1. Keep `main.py` as app entrypoint only.
2. Move ORM model(s) to `models/`.
3. Move Pydantic models to `schemas/`.
4. Move CRUD DB operations to `repositories/`.
5. Move business rules to `services/`.
6. Keep route definitions in `api/`.

## Run Database (Docker Only)

```powershell
docker compose up -d postgres
```

PostgreSQL is exposed on host `localhost:55432`.

## Run API Locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variable

`DATABASE_URL` (optional):

`postgresql+psycopg2://postgres:postgres@localhost:55432/decentrathon`

## Endpoints

- `GET /` health message
- `POST /items` create item
- `GET /items` list items
- `GET /items/{item_id}` get item
- `PUT /items/{item_id}` update item
- `DELETE /items/{item_id}` delete item

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

Docs UI:

- `http://127.0.0.1:8000/docs`
