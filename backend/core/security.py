from datetime import datetime, timedelta, UTC
import bcrypt
import jwt

from core.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def _validate_bcrypt_password(password: str) -> None:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be at most 72 UTF-8 bytes for bcrypt")


def hash_password(password: str) -> str:
    _validate_bcrypt_password(password)
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    _validate_bcrypt_password(password)
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False

def create_access_token(sub: str, role: str) -> str:
    exp = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": sub, "role": role, "exp": exp}, JWT_SECRET, algorithm=JWT_ALGORITHM)
