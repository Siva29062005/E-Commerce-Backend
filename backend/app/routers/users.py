from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models import User
from app.models.role import UserRole
from app.schemas import UserAdminCreate, UserAdminOut, UserOut, UserUpdate
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


def _to_admin_out(user: User) -> UserAdminOut:
    return UserAdminOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=UserRole(user.role),
        created_at=user.created_at.isoformat() if user.created_at else "",
    )


@router.get("", response_model=list[UserAdminOut])
def list_users(_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return [_to_admin_out(u) for u in db.query(User).order_by(User.id).all()]


@router.post("", response_model=UserAdminOut, status_code=status.HTTP_201_CREATED)
def create_user(body: UserAdminCreate, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=body.email.lower(),
        name=body.name.strip(),
        hashed_password=hash_password(body.password),
        role=body.role.value,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _to_admin_out(user)


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)


@router.get("/{user_id}", response_model=UserAdminOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.role != UserRole.ADMIN.value and current.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_admin_out(user)


@router.put("/{user_id}", response_model=UserAdminOut)
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    is_admin = current.role == UserRole.ADMIN.value
    if not is_admin and current.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if body.role is not None and not is_admin:
        raise HTTPException(status_code=403, detail="Cannot change role")
    if body.email and body.email.lower() != user.email:
        if db.query(User).filter(User.email == body.email.lower(), User.id != user_id).first():
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = body.email.lower()
    if body.name is not None:
        user.name = body.name.strip()
    if body.password:
        user.hashed_password = hash_password(body.password)
    if body.role is not None and is_admin:
        user.role = body.role.value
    db.commit()
    db.refresh(user)
    return _to_admin_out(user)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    if admin.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
