from sqlalchemy import select
from sqlalchemy.orm import Session

from models.candidate import Candidate


class CandidateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, full_name: str, email: str, city: str) -> Candidate:
        item = Candidate(full_name=full_name, email=email, city=city)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_all(self) -> list[Candidate]:
        return list(self.db.scalars(select(Candidate).order_by(Candidate.id)))

    def get(self, candidate_id: int) -> Candidate | None:
        return self.db.get(Candidate, candidate_id)

    def update(
        self,
        *,
        candidate: Candidate,
        full_name: str | None = None,
        email: str | None = None,
        city: str | None = None,
    ) -> Candidate:
        if full_name is not None:
            candidate.full_name = full_name
        if email is not None:
            candidate.email = email
        if city is not None:
            candidate.city = city

        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)

        return candidate

    def delete(self, *, candidate: Candidate) -> None:
        self.db.delete(candidate)
        self.db.commit()
