import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import JWT_ALGORITHM, JWT_SECRET
from core.database import get_db
from repositories.item_repository import ItemRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.item_service import ItemService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(repository=ItemRepository(db))


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(repository=UserRepository(db))


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        public_id = payload.get("sub")
        if public_id is None:
            raise credentials_error
    except jwt.PyJWTError as exc:
        raise credentials_error from exc

    user = UserRepository(db).get_by_public_id(str(public_id))
    if user is None:
        raise credentials_error
    return user
