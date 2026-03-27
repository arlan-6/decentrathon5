from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.deps import get_candidate_service
from schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate
from services.candidate_service import CandidateService

router = APIRouter()


@router.post("/", response_model=CandidateRead)
async def create_candidate(
    payload: CandidateCreate,
    service: CandidateService = Depends(get_candidate_service),
):
    try:
        return service.create(payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[CandidateRead])
async def list_candidates(
    service: CandidateService = Depends(get_candidate_service),
):
    return service.list_all()


@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: int,
    service: CandidateService = Depends(get_candidate_service),
):
    candidate = service.get(candidate_id=candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


@router.put("/{candidate_id}", response_model=CandidateRead)
async def update_candidate(
    candidate_id: int,
    payload: CandidateUpdate,
    service: CandidateService = Depends(get_candidate_service),
):
    try:
        candidate = service.update(candidate_id=candidate_id, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")

    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: int,
    service: CandidateService = Depends(get_candidate_service),
):
    deleted = service.delete(candidate_id=candidate_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
