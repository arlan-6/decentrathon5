from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.security import get_subject_from_token
from repositories.application_repository import ApplicationRepository
from repositories.candidate_repository import CandidateRepository
from repositories.review_repository import ReviewRepository
from repositories.score_repository import ScoreRepository
from repositories.user_repository import UserRepository
from services.ai_service import AIService
from services.application_service import ApplicationService
from services.auth_service import AuthService
from services.candidate_service import CandidateService
from services.review_service import ReviewService
from services.scoring_service import ScoringService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

user_repository = UserRepository()
candidate_repository = CandidateRepository()
application_repository = ApplicationRepository()
score_repository = ScoreRepository()
review_repository = ReviewRepository()

auth_service = AuthService(user_repository=user_repository)
candidate_service = CandidateService(candidate_repository=candidate_repository)
application_service = ApplicationService(
    application_repository=application_repository,
    candidate_repository=candidate_repository,
)
ai_service = AIService()
scoring_service = ScoringService(
    application_repository=application_repository,
    score_repository=score_repository,
    ai_service=ai_service,
)
review_service = ReviewService(
    application_repository=application_repository,
    review_repository=review_repository,
)


def get_auth_service() -> AuthService:
    return auth_service


def get_candidate_service() -> CandidateService:
    return candidate_service


def get_application_service() -> ApplicationService:
    return application_service


def get_scoring_service() -> ScoringService:
    return scoring_service


def get_review_service() -> ReviewService:
    return review_service


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
):
    subject = get_subject_from_token(token)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = service.get_user_by_email(subject)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

