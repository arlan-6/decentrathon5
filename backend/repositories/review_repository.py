from models.review import Review


class ReviewRepository:
    def __init__(self) -> None:
        self._items: dict[int, Review] = {}
        self._seq = 1

    def create(self, *, application_id: int, reviewer_id: int, rating: int, comment: str) -> Review:
        item = Review(
            id=self._seq,
            application_id=application_id,
            reviewer_id=reviewer_id,
            rating=rating,
            comment=comment,
        )
        self._items[self._seq] = item
        self._seq += 1
        return item

    def list_all(self) -> list[Review]:
        return list(self._items.values())

