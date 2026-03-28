import uuid
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from core.database import Base


class Role(PyEnum):
    ADMIN = "admin"
    CANDIDATE = "candidate"
    REVIEWER = "reviewer"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    public_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum"),
        nullable=False,
        default=Role.CANDIDATE,
    )
