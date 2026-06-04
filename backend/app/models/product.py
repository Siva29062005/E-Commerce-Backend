from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cat: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    old_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    badge: Mapped[str | None] = mapped_column(String(64), nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=4.5)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    img: Mapped[str] = mapped_column(Text, nullable=False)
    img2: Mapped[str] = mapped_column(Text, nullable=False)
    fabric: Mapped[str] = mapped_column(String(255), nullable=False)
    fabric_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    color: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    desc: Mapped[str] = mapped_column(Text, nullable=False)

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(back_populates="product")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")
