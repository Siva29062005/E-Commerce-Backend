from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import Product, User
from app.schemas import ProductCreate, ProductUpdate
from app.services.cloudinary import upload_product_image
from app.services.products import product_to_dict, query_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(
    cat: str | None = Query(None),
    fabric: str | None = Query(None),
    color: str | None = Query(None),
    max_price: int | None = Query(None),
    on_sale: bool = Query(False),
    search: str | None = Query(None),
    sort: str = Query("featured"),
    db: Session = Depends(get_db),
):
    products = query_products(
        db,
        cat=cat,
        fabric=fabric,
        color=color,
        max_price=max_price,
        on_sale=on_sale,
        search=search,
        sort=sort,
    )
    return [product_to_dict(p) for p in products]


@router.get("/meta/categories")
def list_categories(db: Session = Depends(get_db)):
    cats = [r[0] for r in db.query(Product.cat).distinct().order_by(Product.cat).all()]
    return {"categories": cats}


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_dict(product)


@router.post("", status_code=201)
def create_product(body: ProductCreate, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    data = body.model_dump()
    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product_to_dict(product)


@router.post("/upload-image")
async def upload_product_image_endpoint(
    file: UploadFile = File(...),
    _admin: User = Depends(require_admin),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    try:
        url = await upload_product_image(file)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"url": url}


@router.put("/{product_id}")
def update_product(
    product_id: int,
    body: ProductUpdate,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product_to_dict(product)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
