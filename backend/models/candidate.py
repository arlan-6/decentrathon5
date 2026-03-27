from pydantic import BaseModel, EmailStr


class Candidate(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    skills: list[str] = []

