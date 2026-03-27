from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user, get_scoring_service
from schemas.score import ScoreCreate, ScoreRead
from services.scoring_service import ScoringService

router = APIRouter()


@router.post("/", response_model=ScoreRead)
async def score_application(
    payload: ScoreCreate,
    _: object = Depends(get_current_user),
    service: ScoringService = Depends(get_scoring_service),
):
    result = service.score_application(payload=payload)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return result


@router.get("/", response_model=list[ScoreRead])
async def list_scores(
    _: object = Depends(get_current_user),
    service: ScoringService = Depends(get_scoring_service),
):
    return service.list_all()

