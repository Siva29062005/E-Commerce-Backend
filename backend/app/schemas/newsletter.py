from datetime import datetime

from pydantic import BaseModel, EmailStr


class NewsletterCreate(BaseModel):
    email: EmailStr


class NewsletterOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
