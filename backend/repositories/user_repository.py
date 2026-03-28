from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import Role, User

class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        email: str,
        hashed_password: str,
        full_name: str,
        role: Role,
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalars(select(User).where(User.email == email)).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_public_id(self, public_id: str) -> User | None:
        return self.db.scalars(select(User).where(User.public_id == public_id)).first()

