from pydantic import BaseModel, Field


class ScoreCreate(BaseModel):
    application_id: int
    llm_input: str = Field(min_length=3)


class ScoreRead(BaseModel):
    id: int
    application_id: int
    value: float
    rationale: str

