from datetime import datetime

from pydantic import BaseModel, Field


class ReviewOut(BaseModel):
    id: int
    name: str
    loc: str
    tag: str
    review: str
    stars: int
    init: str
    product_id: int | None = None
    user_id: int | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ReviewCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    loc: str = Field(min_length=1, max_length=128)
    review: str = Field(min_length=10)
    stars: int = Field(ge=1, le=5, default=5)
    product_id: int | None = None


class ReviewUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    loc: str | None = Field(None, min_length=1, max_length=128)
    review: str | None = Field(None, min_length=10)
    stars: int | None = Field(None, ge=1, le=5)
    tag: str | None = None
    product_id: int | None = None
