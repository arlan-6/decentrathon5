from repositories.application_repository import ApplicationRepository
from repositories.review_repository import ReviewRepository
from schemas.review import ReviewCreate


class ReviewService:
    def __init__(
        self,
        *,
        application_repository: ApplicationRepository,
        review_repository: ReviewRepository,
    ) -> None:
        self.application_repository = application_repository
        self.review_repository = review_repository

    def create(self, *, payload: ReviewCreate):
        application = self.application_repository.get(payload.application_id)
        if application is None:
            return None
        return self.review_repository.create(
            application_id=payload.application_id,
            reviewer_id=1,
            rating=payload.rating,
            comment=payload.comment,
        )

    def list_all(self):
        return self.review_repository.list_all()

