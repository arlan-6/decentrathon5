from fastapi import APIRouter

from api.v1.endpoints.items import router as items_router

router = APIRouter()
router.include_router(items_router, prefix="/items", tags=["items"])
