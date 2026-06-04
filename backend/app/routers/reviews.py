from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_optional_user, require_admin
from app.models import Review, User
from app.models.role import UserRole
from app.schemas import ReviewCreate, ReviewOut, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _can_modify(review: Review, user: User) -> bool:
    if user.role == UserRole.ADMIN.value:
        return True
    return review.user_id == user.id


@router.get("", response_model=list[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).order_by(Review.created_at.desc()).all()


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("", response_model=ReviewOut, status_code=201)
def create_review(
    body: ReviewCreate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    initials = "".join(w[0].upper() for w in body.name.split()[:2]) or body.name[:2].upper()
    review = Review(
        name=body.name,
        loc=body.loc,
        review=body.review,
        stars=body.stars,
        init=initials,
        tag="Verified Buyer",
        product_id=body.product_id,
        user_id=user.id if user else None,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    body: ReviewUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if not _can_modify(review, user):
        raise HTTPException(status_code=403, detail="Forbidden")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if not _can_modify(review, user):
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(review)
    db.commit()
