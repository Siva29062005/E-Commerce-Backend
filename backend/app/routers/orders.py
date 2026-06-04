from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user, get_optional_user, require_admin
from app.models import CartItem, Order, OrderItem, Product, User
from app.models.order import OrderStatus
from app.models.role import UserRole
from app.schemas import OrderCreate, OrderOut, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])

FREE_SHIPPING_THRESHOLD = 1999
SHIPPING_COST = 99


def _get_order_or_404(order_id: int, db: Session) -> Order:
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def _can_view_order(order: Order, user: User) -> bool:
    if user.role == UserRole.ADMIN.value:
        return True
    return order.user_id == user.id


@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    body: OrderCreate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    subtotal = 0
    order_items: list[OrderItem] = []

    for line in body.items:
        product = db.get(Product, line.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {line.product_id} not found")
        subtotal += product.price * line.qty
        order_items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                size=line.size,
                qty=line.qty,
                unit_price=product.price,
                img=product.img,
            )
        )

    shipping_cost = 0 if subtotal >= FREE_SHIPPING_THRESHOLD else SHIPPING_COST
    total = subtotal + shipping_cost

    order = Order(
        user_id=user.id if user else None,
        status=OrderStatus.CONFIRMED.value,
        shipping_name=body.shipping_name,
        shipping_email=body.shipping_email.lower(),
        shipping_phone=body.shipping_phone,
        shipping_address=body.shipping_address,
        payment_method=body.payment_method,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        total=total,
        items=order_items,
    )
    db.add(order)
    db.commit()

    if user:
        db.query(CartItem).filter(CartItem.user_id == user.id).delete()
        db.commit()

    return _get_order_or_404(order.id, db)


@router.get("", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Order).options(joinedload(Order.items))
    if user.role != UserRole.ADMIN.value:
        q = q.filter(Order.user_id == user.id)
    return q.order_by(Order.created_at.desc()).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order = _get_order_or_404(order_id, db)
    if not _can_view_order(order, user):
        raise HTTPException(status_code=403, detail="Forbidden")
    return order


@router.put("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    body: OrderUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = _get_order_or_404(order_id, db)
    is_admin = user.role == UserRole.ADMIN.value
    if not is_admin and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    data = body.model_dump(exclude_unset=True)
    if not is_admin:
        data.pop("status", None)
    for key, value in data.items():
        if key == "status" and value is not None:
            setattr(order, key, value.value if hasattr(value, "value") else value)
        elif key == "shipping_email" and value:
            setattr(order, key, str(value).lower())
        else:
            setattr(order, key, value)
    db.commit()
    return _get_order_or_404(order_id, db)


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
