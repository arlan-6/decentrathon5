from models.candidate import Candidate


class CandidateRepository:
    def __init__(self) -> None:
        self._items: dict[int, Candidate] = {}
        self._seq = 1

    def create(self, *, full_name: str, email: str, skills: list[str]) -> Candidate:
        item = Candidate(id=self._seq, full_name=full_name, email=email, skills=skills)
        self._items[self._seq] = item
        self._seq += 1
        return item

    def list_all(self) -> list[Candidate]:
        return list(self._items.values())

    def get(self, candidate_id: int) -> Candidate | None:
        return self._items.get(candidate_id)

