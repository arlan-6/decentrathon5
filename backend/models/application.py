from pydantic import BaseModel


class Application(BaseModel):
    id: int
    candidate_id: int
    role: str
    motivation: str
    status: str = "submitted"

