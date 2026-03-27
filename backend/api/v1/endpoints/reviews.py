from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user, get_review_service
from schemas.review import ReviewCreate, ReviewRead
from services.review_service import ReviewService

router = APIRouter()


@router.post("/", response_model=ReviewRead)
async def create_review(
    payload: ReviewCreate,
    _: object = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    result = service.create(payload=payload)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return result


@router.get("/", response_model=list[ReviewRead])
async def list_reviews(
    _: object = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    return service.list_all()

