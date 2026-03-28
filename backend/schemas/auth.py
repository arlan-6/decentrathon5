from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.user import Role

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)
    full_name: str
    role: Role = Role.CANDIDATE

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)

class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = "bearer"

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(validation_alias="public_id")
    email: EmailStr
    full_name: str
    role: Role
