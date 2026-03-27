from models.score import Score


class ScoreRepository:
    def __init__(self) -> None:
        self._items: dict[int, Score] = {}
        self._seq = 1

    def create(self, *, application_id: int, value: float, rationale: str) -> Score:
        item = Score(id=self._seq, application_id=application_id, value=value, rationale=rationale)
        self._items[self._seq] = item
        self._seq += 1
        return item

    def list_all(self) -> list[Score]:
        return list(self._items.values())

