from datetime import date

import jwt
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_locale, get_today
from src.core.config import FRONTEND_URL
from src.core.email import send_email
from src.core.security import (
    check_reset_token,
    create_access_token,
    create_reset_token,
    reset_token_user_id,
    verify_password,
)
from src.crud import badge as badge_crud
from src.crud import user as user_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.auth import ForgotPasswordData, LoginData, ResetPasswordData, Token
from src.schemas.user import UserCreate, UserRead

router = APIRouter()

RESET_EMAIL = {
    "en": (
        "Reset your Polycode password",
        "Hi {username},\n\nOpen this link within an hour to choose a new password:\n{link}\n\n"
        "If you didn't ask for this, you can ignore this email.",
    ),
    "pl": (
        "Zresetuj hasło do Polycode",
        "Cześć {username},\n\nOtwórz ten link w ciągu godziny, aby ustawić nowe hasło:\n{link}\n\n"
        "Jeśli to nie Ty, zignoruj tę wiadomość.",
    ),
}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account with hashed password."""
    if user_crud.get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken.",
        )
    if user_crud.get_user_by_email(db, str(user_in.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    return user_crud.create_user(db, user_in)


@router.post("/login", response_model=Token)
def login(
    login_data: LoginData, db: Session = Depends(get_db), today: date = Depends(get_today)
):
    """Authenticate user with username/email and password, returning JWT access token.

    Also awards badges the user already qualifies for, e.g. ones added after they earned them.
    """
    user = user_crud.get_user_by_identifier(db, login_data.username_or_email)

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    badge_crud.sync_badges(db, user, today)
    db.commit()

    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/forgot-password", status_code=status.HTTP_204_NO_CONTENT)
def forgot_password(
    data: ForgotPasswordData,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale),
):
    """Email a password reset link.

    The answer is the same whether or not the email is registered, so it can't be used to find
    accounts; the email is sent after the response for the same reason.
    """
    user = user_crud.get_user_by_email(db, str(data.email))
    if user:
        subject, body = RESET_EMAIL.get(locale, RESET_EMAIL["en"])
        link = f"{FRONTEND_URL}/reset-password?token={create_reset_token(user.id, user.password)}"
        background_tasks.add_task(
            send_email, user.email, subject, body.format(username=user.username, link=link)
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(data: ResetPasswordData, db: Session = Depends(get_db)):
    """Set a new password using the token from a reset link; each link works once."""
    try:
        user = user_crud.get_user_by_id(db, reset_token_user_id(data.token))
        if user is None:
            raise ValueError
        check_reset_token(data.token, user.password)
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This reset link is invalid or has expired.",
        )
    user_crud.update_password(db, user, data.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserRead)
def get_current_user_profile(
    current_user: User = Depends(get_current_user), today: date = Depends(get_today)
):
    """Retrieve profile of the currently authenticated user (JWT protected).

    A streak broken by a skipped day reads as 0, so the header never shows a stale one.
    """
    return user_crud.user_read(current_user, today)
