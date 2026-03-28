from datetime import datetime, timedelta, UTC
import hashlib
import uuid
from typing import Any
import bcrypt
import jwt

from core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


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
    return jwt.encode(
        {"sub": sub, "role": role, "type": "access", "exp": exp},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def create_refresh_token(sub: str) -> tuple[str, str, datetime]:
    jti = str(uuid.uuid4())
    exp = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode(
        {"sub": sub, "type": "refresh", "jti": jti, "exp": exp},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return token, jti, exp


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    token_type = payload.get("type")
    if expected_type is not None and token_type != expected_type:
        raise jwt.InvalidTokenError("Invalid token type")
    return payload


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
