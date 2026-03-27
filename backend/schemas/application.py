from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    candidate_id: int
    role: str
    motivation: str


class ApplicationRead(BaseModel):
    id: int
    candidate_id: int
    role: str
    motivation: str
    status: str

