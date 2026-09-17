from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.security import create_access_token, verify_password
from src.crud import user as user_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.auth import LoginData, Token
from src.schemas.user import UserCreate, UserRead

router = APIRouter()


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
def login(login_data: LoginData, db: Session = Depends(get_db)):
    """Authenticate user with username/email and password, returning JWT access token."""
    user = user_crud.get_user_by_identifier(db, login_data.username_or_email)

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email/username or password",
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
