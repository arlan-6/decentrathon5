from models.user import User


def hash_password(password: str) -> str:
    return f"hashed::{password}"


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


def create_access_token(user: User) -> str:
    return f"token::{user.email}"


def get_subject_from_token(token: str) -> str | None:
    if not token.startswith("token::"):
        return None
    return token.replace("token::", "", 1)

