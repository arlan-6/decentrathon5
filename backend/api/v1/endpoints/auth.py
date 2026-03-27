from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_auth_service, get_current_user
from schemas.auth import TokenResponse, UserCreate, UserLogin, UserRead
from services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(payload: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return service.register(payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, service: AuthService = Depends(get_auth_service)):
    token = service.login(payload=payload)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user

