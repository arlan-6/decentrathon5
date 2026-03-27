from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.router import router as v1_router
from core.database import init_db
from core.logging import configure_logging

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Decentrathon Backend", version="0.1.0", lifespan=lifespan)
app.include_router(v1_router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    return {"message": "Decentrathon backend is running"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
