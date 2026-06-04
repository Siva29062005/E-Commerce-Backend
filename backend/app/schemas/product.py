from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    cat: str
    price: int = Field(ge=0)
    old_price: int | None = Field(None, ge=0)
    badge: str | None = None
    rating: float = Field(default=4.5, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    img: str
    img2: str
    fabric: str
    fabric_type: str
    color: str
    tags: list[str] = []
    desc: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    cat: str | None = None
    price: int | None = Field(None, ge=0)
    old_price: int | None = None
    badge: str | None = None
    rating: float | None = Field(None, ge=0, le=5)
    review_count: int | None = Field(None, ge=0)
    img: str | None = None
    img2: str | None = None
    fabric: str | None = None
    fabric_type: str | None = None
    color: str | None = None
    tags: list[str] | None = None
    desc: str | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    cat: str
    price: int
    oldPrice: int | None = None
    badge: str | None = None
    rating: float
    reviews: int
    img: str
    img2: str
    fabric: str
    fabricType: str
    color: str
    tags: list[str]
    desc: str
