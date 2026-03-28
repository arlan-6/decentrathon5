from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import get_auth_service, get_current_user
from models.user import User
from schemas.auth import RegisterRequest, TokenResponse, UserRead
from services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.register(payload)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return service.login(email=form_data.username, password=form_data.password)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user
