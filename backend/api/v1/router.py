from fastapi import APIRouter

from api.v1.endpoints.applications import router as applications_router
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.candidates import router as candidates_router
from api.v1.endpoints.health import router as health_router
from api.v1.endpoints.reviews import router as reviews_router
from api.v1.endpoints.scoring import router as scoring_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(candidates_router, prefix="/candidates", tags=["candidates"])
router.include_router(applications_router, prefix="/applications", tags=["applications"])
router.include_router(scoring_router, prefix="/scoring", tags=["scoring"])
router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])

