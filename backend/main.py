from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.router import router as v1_router
from core.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Simple CRUD API", version="1.0.0", lifespan=lifespan)
app.include_router(v1_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "API is running"}
