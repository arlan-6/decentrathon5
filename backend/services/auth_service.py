from fastapi import HTTPException, status
import jwt

from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)
from models.user import User
from repositories.refresh_token_repository import RefreshTokenRepository
from repositories.user_repository import UserRepository
from schemas.auth import RefreshTokenRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(
        self,
        repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ) -> None:
        self.repository = repository
        self.refresh_repository = refresh_repository

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
        return self._issue_tokens(user)

    def refresh(self, payload: RefreshTokenRequest) -> TokenResponse:
        refresh_token = payload.refresh_token
        credentials_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

        try:
            token_payload = decode_token(refresh_token, expected_type="refresh")
        except jwt.PyJWTError as exc:
            raise credentials_error from exc

        public_id = token_payload.get("sub")
        jti = token_payload.get("jti")
        if public_id is None or jti is None:
            raise credentials_error

        consumed = self.refresh_repository.consume(
            jti=str(jti),
            token_hash=hash_token(refresh_token),
        )
        if consumed is None:
            raise credentials_error

        user = self.repository.get_by_public_id(str(public_id))
        if user is None:
            raise credentials_error

        return self._issue_tokens(user)

    def logout(self, payload: RefreshTokenRequest) -> None:
        credentials_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

        try:
            token_payload = decode_token(payload.refresh_token, expected_type="refresh")
        except jwt.PyJWTError as exc:
            raise credentials_error from exc

        jti = token_payload.get("jti")
        if jti is None:
            raise credentials_error

        self.refresh_repository.revoke_by_jti(str(jti))

    def _issue_tokens(self, user: User) -> TokenResponse:
        access_token = create_access_token(sub=user.public_id, role=user.role.value)
        refresh_token, jti, refresh_expires_at = create_refresh_token(sub=user.public_id)
        self.refresh_repository.create(
            jti=jti,
            token_hash=hash_token(refresh_token),
            user_public_id=user.public_id,
            expires_at=refresh_expires_at,
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
