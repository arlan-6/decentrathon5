from core.security import create_access_token, hash_password, verify_password
from repositories.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin


class AuthService:
    def __init__(self, *, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, *, payload: UserCreate):
        if self.user_repository.get_by_email(payload.email):
            raise ValueError("Email already exists")
        user = self.user_repository.create(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role=payload.role,
        )
        return {"id": user.id, "email": user.email, "role": user.role}

    def login(self, *, payload: UserLogin) -> str | None:
        user = self.user_repository.get_by_email(payload.email)
        if user is None:
            return None
        if not verify_password(payload.password, user.hashed_password):
            return None
        return create_access_token(user)

    def get_user_by_email(self, email: str):
        user = self.user_repository.get_by_email(email)
        if user is None:
            return None
        return {"id": user.id, "email": user.email, "role": user.role}

