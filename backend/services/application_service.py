from repositories.application_repository import ApplicationRepository
from repositories.candidate_repository import CandidateRepository
from schemas.application import ApplicationCreate, ApplicationUpdate


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
            essay_text=payload.essay_text,
            motivation_text=payload.motivation_text,
        )

    def list_all(self):
        return self.application_repository.list_all()

    def get(self, *, application_id: int):
        return self.application_repository.get(application_id)

    def update(self, *, application_id: int, payload: ApplicationUpdate):
        application = self.application_repository.get(application_id)
        if application is None:
            return None

        return self.application_repository.update(
            application=application,
            essay_text=payload.essay_text,
            motivation_text=payload.motivation_text,
            status=payload.status,
        )

    def delete(self, *, application_id: int) -> bool:
        application = self.application_repository.get(application_id)
        if application is None:
            return False

        self.application_repository.delete(application=application)
        return True
