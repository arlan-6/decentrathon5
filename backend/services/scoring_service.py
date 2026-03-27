from repositories.application_repository import ApplicationRepository
from repositories.score_repository import ScoreRepository
from schemas.score import ScoreCreate
from services.ai_service import AIService


class ScoringService:
    def __init__(
        self,
        *,
        application_repository: ApplicationRepository,
        score_repository: ScoreRepository,
        ai_service: AIService,
    ) -> None:
        self.application_repository = application_repository
        self.score_repository = score_repository
        self.ai_service = ai_service

    def score_application(self, *, payload: ScoreCreate):
        application = self.application_repository.get(payload.application_id)
        if application is None:
            return None
        value, rationale = self.ai_service.evaluate(payload.llm_input)
        return self.score_repository.create(
            application_id=payload.application_id,
            value=value,
            rationale=rationale,
        )

    def list_all(self):
        return self.score_repository.list_all()

