from fastapi import APIRouter, Depends

from api.deps import get_application_service, get_current_user
from schemas.application import ApplicationCreate, ApplicationRead
from services.application_service import ApplicationService

router = APIRouter()


@router.post("/", response_model=ApplicationRead)
async def create_application(
    payload: ApplicationCreate,
    _: object = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.create(payload=payload)


@router.get("/", response_model=list[ApplicationRead])
async def list_applications(
    _: object = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    return service.list_all()

