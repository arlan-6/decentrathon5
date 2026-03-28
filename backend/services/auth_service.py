from fastapi import HTTPException, status

from core.security import create_access_token, hash_password, verify_password
from models.user import User
from repositories.user_repository import UserRepository
from schemas.auth import RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def register(self, payload: RegisterRequest) -> User:
        existing = self.repository.get_by_email(payload.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        try:
            hashed_password = hash_password(payload.password)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at most 72 UTF-8 bytes for bcrypt",
            ) from exc
        return self.repository.create(
            email=str(payload.email),
            hashed_password=hashed_password,
            full_name=payload.full_name,
            role=payload.role,
        )

    def login(self, *, email: str, password: str) -> TokenResponse:
        user = self.repository.get_by_email(email)
        try:
            valid_password = user is not None and verify_password(password, user.hashed_password)
        except ValueError:
            valid_password = False
        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = create_access_token(sub=user.public_id, role=user.role.value)
        return TokenResponse(access_token=token)
