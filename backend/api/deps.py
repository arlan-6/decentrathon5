from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.application_repository import ApplicationRepository
from repositories.candidate_repository import CandidateRepository
from services.application_service import ApplicationService
from services.candidate_service import CandidateService


def get_candidate_service(db: Session = Depends(get_db)) -> CandidateService:
    candidate_repository = CandidateRepository(db)
    return CandidateService(candidate_repository=candidate_repository)


def get_application_service(db: Session = Depends(get_db)) -> ApplicationService:
    application_repository = ApplicationRepository(db)
    candidate_repository = CandidateRepository(db)
    return ApplicationService(
        application_repository=application_repository,
        candidate_repository=candidate_repository,
    )
