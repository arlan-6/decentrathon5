from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    candidate_id: int
    essay_text: str
    motivation_text: str


class ApplicationUpdate(BaseModel):
    essay_text: str | None = None
    motivation_text: str | None = None
    status: str | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_id: int
    essay_text: str
    motivation_text: str
    status: str
    submitted_at: datetime
