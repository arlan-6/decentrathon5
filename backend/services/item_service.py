from repositories.item_repository import ItemRepository
from schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, *, repository: ItemRepository) -> None:
        self.repository = repository

    def create(self, *, payload: ItemCreate):
        return self.repository.create(name=payload.name)

    def list_all(self):
        return self.repository.list_all()

    def get(self, *, item_id: int):
        return self.repository.get(item_id)

    def update(self, *, item_id: int, payload: ItemUpdate):
        item = self.repository.get(item_id)
        if item is None:
            return None
        return self.repository.update(item=item, name=payload.name)

    def delete(self, *, item_id: int) -> bool:
        item = self.repository.get(item_id)
        if item is None:
            return False
        self.repository.delete(item=item)
        return True
