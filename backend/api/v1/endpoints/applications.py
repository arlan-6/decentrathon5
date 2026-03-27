from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.deps import get_application_service
from schemas.application import ApplicationCreate, ApplicationRead, ApplicationUpdate
from services.application_service import ApplicationService

router = APIRouter()


@router.post("/", response_model=ApplicationRead)
async def create_application(
    payload: ApplicationCreate,
    service: ApplicationService = Depends(get_application_service),
):
    try:
        return service.create(payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[ApplicationRead])
async def list_applications(
    service: ApplicationService = Depends(get_application_service),
):
    return service.list_all()


@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application(
    application_id: int,
    service: ApplicationService = Depends(get_application_service),
):
    application = service.get(application_id=application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.put("/{application_id}", response_model=ApplicationRead)
async def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    service: ApplicationService = Depends(get_application_service),
):
    application = service.update(application_id=application_id, payload=payload)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    service: ApplicationService = Depends(get_application_service),
):
    deleted = service.delete(application_id=application_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
