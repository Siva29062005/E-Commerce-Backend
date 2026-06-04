from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models import Product, User, WishlistItem
from app.services.products import product_to_dict

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get("")
def get_wishlist(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = (
        db.query(WishlistItem)
        .options(joinedload(WishlistItem.product))
        .filter(WishlistItem.user_id == user.id)
        .all()
    )
    return [{"id": i.id, "product_id": i.product_id, "product": product_to_dict(i.product)} for i in items]


@router.get("/{product_id}")
def get_wishlist_item(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = (
        db.query(WishlistItem)
        .options(joinedload(WishlistItem.product))
        .filter(WishlistItem.user_id == user.id, WishlistItem.product_id == product_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Not in wishlist")
    return {"id": item.id, "product_id": item.product_id, "product": product_to_dict(item.product)}


@router.post("/{product_id}", status_code=201)
def add_to_wishlist(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Product, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    existing = (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user.id, WishlistItem.product_id == product_id)
        .first()
    )
    if existing:
        return {"product_id": product_id}
    item = WishlistItem(user_id=user.id, product_id=product_id)
    db.add(item)
    db.commit()
    return {"product_id": product_id}


@router.delete("/{product_id}", status_code=204)
def remove_from_wishlist(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user.id, WishlistItem.product_id == product_id)
        .first()
    )
    if item:
        db.delete(item)
        db.commit()
