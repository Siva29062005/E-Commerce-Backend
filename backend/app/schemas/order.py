from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.order import OrderStatus


class OrderItemInput(BaseModel):
    product_id: int
    size: str
    qty: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    items: list[OrderItemInput] = Field(min_length=1)
    shipping_name: str = Field(min_length=1, max_length=255)
    shipping_email: EmailStr
    shipping_phone: str = Field(min_length=6, max_length=32)
    shipping_address: str = ""
    payment_method: str = "card"


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None
    shipping_name: str | None = None
    shipping_email: EmailStr | None = None
    shipping_phone: str | None = None
    shipping_address: str | None = None


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    size: str
    qty: int
    unit_price: int
    img: str

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    user_id: int | None
    status: str
    shipping_name: str
    shipping_email: str
    shipping_phone: str
    shipping_address: str
    payment_method: str
    subtotal: int
    shipping_cost: int
    total: int
    created_at: datetime
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}
