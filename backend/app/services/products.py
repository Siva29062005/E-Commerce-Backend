from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Product


def product_to_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "cat": p.cat,
        "price": p.price,
        "oldPrice": p.old_price,
        "badge": p.badge,
        "rating": p.rating,
        "reviews": p.review_count,
        "img": p.img,
        "img2": p.img2,
        "fabric": p.fabric,
        "fabricType": p.fabric_type,
        "color": p.color,
        "tags": p.tags or [],
        "desc": p.desc,
    }


def query_products(
    db: Session,
    *,
    cat: str | None = None,
    fabric: str | None = None,
    color: str | None = None,
    max_price: int | None = None,
    on_sale: bool = False,
    search: str | None = None,
    sort: str = "featured",
) -> list[Product]:
    q = db.query(Product)

    if cat and cat != "All":
        q = q.filter(Product.cat == cat)
    if fabric and fabric != "All":
        q = q.filter(Product.fabric_type == fabric)
    if color and color != "All":
        q = q.filter(Product.color == color)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)
    if on_sale:
        q = q.filter(Product.old_price.isnot(None))
    if search:
        term = f"%{search.lower()}%"
        q = q.filter(
            or_(
                Product.name.ilike(term),
                Product.cat.ilike(term),
                Product.fabric_type.ilike(term),
                Product.desc.ilike(term),
            )
        )

    products = q.all()

    if sort == "price-asc":
        products.sort(key=lambda p: p.price)
    elif sort == "price-desc":
        products.sort(key=lambda p: p.price, reverse=True)
    elif sort == "rating":
        products.sort(key=lambda p: p.rating, reverse=True)
    elif sort == "name":
        products.sort(key=lambda p: p.name.lower())

    return products
