from fastapi import APIRouter

from api.v1.endpoints.applications import router as applications_router
from api.v1.endpoints.candidates import router as candidates_router
from api.v1.endpoints.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(candidates_router, prefix="/candidates", tags=["candidates"])
router.include_router(applications_router, prefix="/applications", tags=["applications"])
