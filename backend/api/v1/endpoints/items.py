from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.deps import get_current_user, get_item_service
from schemas.item import ItemCreate, ItemRead, ItemUpdate
from services.item_service import ItemService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service),
):
    return service.create(payload=payload)


@router.get("/", response_model=list[ItemRead])
def list_items(service: ItemService = Depends(get_item_service)):
    return service.list_all()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
):
    item = service.get(item_id=item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
):
    item = service.update(item_id=item_id, payload=payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
):
    deleted = service.delete(item_id=item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
