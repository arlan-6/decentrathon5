from models.application import Application


class ApplicationRepository:
    def __init__(self) -> None:
        self._items: dict[int, Application] = {}
        self._seq = 1

    def create(self, *, candidate_id: int, role: str, motivation: str) -> Application:
        item = Application(
            id=self._seq,
            candidate_id=candidate_id,
            role=role,
            motivation=motivation,
        )
        self._items[self._seq] = item
        self._seq += 1
        return item

    def list_all(self) -> list[Application]:
        return list(self._items.values())

    def get(self, application_id: int) -> Application | None:
        return self._items.get(application_id)

