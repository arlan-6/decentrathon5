from pydantic import BaseModel


class Score(BaseModel):
    id: int
    application_id: int
    value: float
    rationale: str

