from pydantic import BaseModel, EmailStr, Field

from app.models.role import UserRole


class UserAdminCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6, max_length=128)
    role: UserRole | None = None


class UserAdminOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: str

    model_config = {"from_attributes": True}
