from pydantic import BaseModel, Field

from app.schemas.product import ProductOut


class CartItemCreate(BaseModel):
    product_id: int
    size: str = Field(min_length=1, max_length=8)
    qty: int = Field(ge=1, le=99, default=1)


class CartItemUpdate(BaseModel):
    qty: int = Field(ge=1, le=99)


class CartItemOut(BaseModel):
    id: int
    product_id: int
    size: str
    qty: int
    product: ProductOut

    model_config = {"from_attributes": True}
