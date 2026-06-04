from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import ContactMessage, User
from app.schemas import ContactCreate, ContactOut

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ContactOut, status_code=201)
def submit_contact(body: ContactCreate, db: Session = Depends(get_db)):
    msg = ContactMessage(
        name=body.name.strip(),
        email=body.email.lower(),
        subject=body.subject.strip(),
        message=body.message.strip(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.get("", response_model=list[ContactOut])
def list_contact_messages(_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()


@router.get("/{message_id}", response_model=ContactOut)
def get_contact_message(message_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    msg = db.get(ContactMessage, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.delete("/{message_id}", status_code=204)
def delete_contact_message(message_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    msg = db.get(ContactMessage, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
