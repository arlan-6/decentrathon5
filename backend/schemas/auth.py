from pydantic import BaseModel, EmailStr

from utils.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.REVIEWER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

