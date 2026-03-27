from fastapi import FastAPI

from api.v1.router import router as v1_router
from core.logging import configure_logging

configure_logging()

app = FastAPI(title="Decentrathon Backend", version="0.1.0")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    return {"message": "Decentrathon backend is running"}

