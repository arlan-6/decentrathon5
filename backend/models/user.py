from pydantic import BaseModel, EmailStr

from utils.enums import UserRole


class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    role: UserRole = UserRole.REVIEWER

