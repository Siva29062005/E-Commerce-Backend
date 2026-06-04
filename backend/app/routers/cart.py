from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models import CartItem, Product, User
from app.schemas import CartItemCreate, CartItemUpdate
from app.services.products import product_to_dict

router = APIRouter(prefix="/cart", tags=["cart"])


def _cart_item_out(item: CartItem) -> dict:
    return {
        "id": item.id,
        "product_id": item.product_id,
        "size": item.size,
        "qty": item.qty,
        "product": product_to_dict(item.product),
    }


@router.get("")
def get_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user.id)
        .all()
    )
    return [_cart_item_out(i) for i in items]


@router.get("/{item_id}")
def get_cart_item(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.id == item_id, CartItem.user_id == user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return _cart_item_out(item)


@router.post("", status_code=201)
def add_to_cart(body: CartItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.get(Product, body.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == user.id,
            CartItem.product_id == body.product_id,
            CartItem.size == body.size,
        )
        .first()
    )
    if existing:
        existing.qty = min(99, existing.qty + body.qty)
        db.commit()
        item = db.query(CartItem).options(joinedload(CartItem.product)).get(existing.id)
        return _cart_item_out(item)
    item = CartItem(user_id=user.id, product_id=body.product_id, size=body.size, qty=body.qty)
    db.add(item)
    db.commit()
    item = db.query(CartItem).options(joinedload(CartItem.product)).get(item.id)
    return _cart_item_out(item)


@router.put("/{item_id}")
def replace_cart_item(
    item_id: int,
    body: CartItemCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if not db.get(Product, body.product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    item.product_id = body.product_id
    item.size = body.size
    item.qty = body.qty
    db.commit()
    item = db.query(CartItem).options(joinedload(CartItem.product)).get(item_id)
    return _cart_item_out(item)


@router.patch("/{item_id}")
def update_cart_item(
    item_id: int,
    body: CartItemUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.id == item_id, CartItem.user_id == user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.qty = body.qty
    db.commit()
    db.refresh(item)
    return _cart_item_out(item)


@router.delete("/{item_id}", status_code=204)
def remove_cart_item(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()


@router.delete("", status_code=204)
def clear_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
