from repositories.candidate_repository import CandidateRepository
from schemas.candidate import CandidateCreate


class CandidateService:
    def __init__(self, *, candidate_repository: CandidateRepository) -> None:
        self.candidate_repository = candidate_repository

    def create(self, *, payload: CandidateCreate):
        return self.candidate_repository.create(
            full_name=payload.full_name,
            email=payload.email,
            skills=payload.skills,
        )

    def list_all(self):
        return self.candidate_repository.list_all()

