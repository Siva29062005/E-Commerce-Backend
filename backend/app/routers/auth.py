from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config import settings
from app.cookies import REFRESH_COOKIE, clear_refresh_cookie, set_refresh_cookie
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.models.role import UserRole
from app.schemas import AccessTokenResponse, TokenResponse, UserCreate, UserLogin, UserOut
from app.security import create_access_token, hash_password, verify_password
from app.services.auth_tokens import (
    create_refresh_session,
    revoke_all_user_tokens,
    revoke_refresh_token,
    rotate_refresh_session,
    validate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _token_response(user: User, access: str) -> dict:
    return {
        "access_token": access,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": UserOut.model_validate(user),
    }


def _issue_tokens(response: Response, user: User, db: Session) -> dict:
    access = create_access_token(str(user.id), user.role)
    refresh = create_refresh_session(db, user)
    set_refresh_cookie(response, refresh)
    return _token_response(user, access)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, response: Response, db: Session = Depends(get_db)):
    if body.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Cannot self-register as admin")
    if db.query(User).filter(User.email == body.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=body.email.lower(),
        name=body.name.strip(),
        hashed_password=hash_password(body.password),
        role=UserRole.USER.value,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(**_issue_tokens(response, user, db))


@router.post("/login")
def login(body: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower()).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    revoke_all_user_tokens(db, user.id)
    return TokenResponse(**_issue_tokens(response, user, db))


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(None, alias=REFRESH_COOKIE),
):
    user = validate_refresh_token(db, refresh_token or "")
    if not user:
        clear_refresh_cookie(response)
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    new_refresh = rotate_refresh_session(db, user, refresh_token or "")
    set_refresh_cookie(response, new_refresh)
    access = create_access_token(str(user.id), user.role)
    return AccessTokenResponse(
        access_token=access,
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(None, alias=REFRESH_COOKIE),
):
    if refresh_token:
        revoke_refresh_token(db, refresh_token)
    clear_refresh_cookie(response)


@router.post("/logout-all", status_code=204)
def logout_all(
    response: Response,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    revoke_all_user_tokens(db, user.id)
    clear_refresh_cookie(response)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)
