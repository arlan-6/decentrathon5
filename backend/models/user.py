from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from utils.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default=UserRole.REVIEWER.value)
