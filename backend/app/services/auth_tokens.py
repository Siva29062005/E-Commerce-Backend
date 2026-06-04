import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.models import RefreshToken, User


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def create_refresh_session(db: Session, user: User) -> str:
    plain = generate_refresh_token()
    expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=_hash_token(plain),
            expires_at=expires,
        )
    )
    db.commit()
    return plain


def revoke_refresh_token(db: Session, plain: str) -> None:
    row = db.query(RefreshToken).filter(RefreshToken.token_hash == _hash_token(plain)).first()
    if row and row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        db.commit()


def revoke_all_user_tokens(db: Session, user_id: int) -> None:
    now = datetime.now(timezone.utc)
    rows = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None),
    ).all()
    for row in rows:
        row.revoked_at = now
    db.commit()


def validate_refresh_token(db: Session, plain: str) -> User | None:
    if not plain:
        return None
    row = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == _hash_token(plain))
        .first()
    )
    if not row or row.revoked_at is not None:
        return None
    expires = row.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < datetime.now(timezone.utc):
        return None
    return db.get(User, row.user_id)


def rotate_refresh_session(db: Session, user: User, old_plain: str) -> str:
    revoke_refresh_token(db, old_plain)
    return create_refresh_session(db, user)
