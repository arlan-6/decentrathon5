from fastapi import APIRouter, Depends

from api.deps import get_candidate_service, get_current_user
from schemas.candidate import CandidateCreate, CandidateRead
from services.candidate_service import CandidateService

router = APIRouter()


@router.post("/", response_model=CandidateRead)
async def create_candidate(
    payload: CandidateCreate,
    _: object = Depends(get_current_user),
    service: CandidateService = Depends(get_candidate_service),
):
    return service.create(payload=payload)


@router.get("/", response_model=list[CandidateRead])
async def list_candidates(
    _: object = Depends(get_current_user),
    service: CandidateService = Depends(get_candidate_service),
):
    return service.list_all()

