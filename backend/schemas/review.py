from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    application_id: int
    rating: int = Field(ge=1, le=5)
    comment: str


class ReviewRead(BaseModel):
    id: int
    application_id: int
    reviewer_id: int
    rating: int
    comment: str

