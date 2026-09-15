from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.security import create_access_token, hash_password, verify_password
from src.model.db import get_db
from src.model.user import User
from src.schemas.auth import LoginData, Token
from src.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account with hashed password."""
    existing_user = (
        db.query(User)
        .filter(or_(User.username == user_in.username, User.email == user_in.email))
        .first()
    )
    if existing_user:
        if existing_user.username == user_in.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    user = User(
        username=user_in.username,
        email=str(user_in.email),
        password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(login_data: LoginData, db: Session = Depends(get_db)):
    """Authenticate user with username/email and password, returning JWT access token."""
    identifier = login_data.username_or_email
    user = (
        db.query(User)
        .filter(or_(User.username == identifier, User.email == identifier))
        .first()
    )

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieve profile of the currently authenticated user (JWT protected)."""
    return current_user
