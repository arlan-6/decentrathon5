from repositories.candidate_repository import CandidateRepository
from schemas.candidate import CandidateCreate, CandidateUpdate


class CandidateService:
    def __init__(self, *, candidate_repository: CandidateRepository) -> None:
        self.candidate_repository = candidate_repository

    def create(self, *, payload: CandidateCreate):
        existing = next(
            (
                candidate
                for candidate in self.candidate_repository.list_all()
                if candidate.email == str(payload.email)
            ),
            None,
        )
        if existing is not None:
            raise ValueError("Candidate email already exists")

        return self.candidate_repository.create(
            full_name=payload.full_name,
            email=str(payload.email),
            city=payload.city,
        )

    def list_all(self):
        return self.candidate_repository.list_all()

    def get(self, *, candidate_id: int):
        return self.candidate_repository.get(candidate_id)

    def update(self, *, candidate_id: int, payload: CandidateUpdate):
        candidate = self.candidate_repository.get(candidate_id)
        if candidate is None:
            return None

        if payload.email is not None:
            for existing_candidate in self.candidate_repository.list_all():
                if existing_candidate.id != candidate_id and existing_candidate.email == str(
                    payload.email
                ):
                    raise ValueError("Candidate email already exists")

        return self.candidate_repository.update(
            candidate=candidate,
            full_name=payload.full_name,
            email=str(payload.email) if payload.email is not None else None,
            city=payload.city,
        )

    def delete(self, *, candidate_id: int) -> bool:
        candidate = self.candidate_repository.get(candidate_id)
        if candidate is None:
            return False

        self.candidate_repository.delete(candidate=candidate)
        return True
