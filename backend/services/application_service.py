from repositories.application_repository import ApplicationRepository
from repositories.candidate_repository import CandidateRepository
from schemas.application import ApplicationCreate


class ApplicationService:
    def __init__(
        self,
        *,
        application_repository: ApplicationRepository,
        candidate_repository: CandidateRepository,
    ) -> None:
        self.application_repository = application_repository
        self.candidate_repository = candidate_repository

    def create(self, *, payload: ApplicationCreate):
        if self.candidate_repository.get(payload.candidate_id) is None:
            raise ValueError("Candidate does not exist")
        return self.application_repository.create(
            candidate_id=payload.candidate_id,
            role=payload.role,
            motivation=payload.motivation,
        )

    def list_all(self):
        return self.application_repository.list_all()

