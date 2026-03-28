from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.item_repository import ItemRepository
from services.item_service import ItemService


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(repository=ItemRepository(db))
