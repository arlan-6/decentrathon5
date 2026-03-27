from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    skills: list[str] = []


class CandidateRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    skills: list[str]

