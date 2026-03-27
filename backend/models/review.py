from pydantic import BaseModel


class Review(BaseModel):
    id: int
    application_id: int
    reviewer_id: int
    rating: int
    comment: str

