from models.user import User


class UserRepository:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._seq = 1

    def create(self, *, email: str, hashed_password: str, role) -> User:
        user = User(id=self._seq, email=email, hashed_password=hashed_password, role=role)
        self._users[self._seq] = user
        self._seq += 1
        return user

    def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._users.values() if u.email == email), None)

