from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    city: str


class CandidateUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    city: str | None = None


class CandidateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    city: str
    created_at: datetime
