from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import NewsletterSubscriber, User
from app.schemas import NewsletterCreate, NewsletterOut

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("", status_code=201)
def subscribe(body: NewsletterCreate, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.query(NewsletterSubscriber).filter(NewsletterSubscriber.email == email).first():
        return {"message": "Already subscribed"}
    sub = NewsletterSubscriber(email=email)
    db.add(sub)
    db.commit()
    return {"message": "Subscribed successfully"}


@router.get("", response_model=list[NewsletterOut])
def list_subscribers(_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(NewsletterSubscriber).order_by(NewsletterSubscriber.created_at.desc()).all()


@router.get("/{subscriber_id}", response_model=NewsletterOut)
def get_subscriber(subscriber_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    sub = db.get(NewsletterSubscriber, subscriber_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return sub


@router.delete("/{subscriber_id}", status_code=204)
def delete_subscriber(subscriber_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    sub = db.get(NewsletterSubscriber, subscriber_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    db.delete(sub)
    db.commit()
