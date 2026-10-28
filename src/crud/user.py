from datetime import date

from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.core.streak import displayed_streak
from src.model.track import Track
from src.model.user import User
from src.schemas.user import UserCreate, UserRead


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Retrieve a user by their primary key ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Retrieve a user by their unique username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by their unique email address."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_identifier(db: Session, identifier: str) -> User | None:
    """Retrieve a user by identifier avoiding email vs username collisions.

    If '@' is present in the identifier, queries exclusively by email.
    Otherwise, queries exclusively by username.
    """
    if "@" in identifier:
        return get_user_by_email(db, identifier)
    return get_user_by_username(db, identifier)


def create_user(db: Session, user_in: UserCreate) -> User:
    """Hash the password and persist a new user record in the database."""
    user = User(
        username=user_in.username,
        email=str(user_in.email),
        password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_read(user: User, today: date) -> UserRead:
    """Return the user as the API shows it: a streak broken by a skipped day reads as 0.

    Only the response changes; the stored streak is left alone, so reads never write.
    """
    return UserRead.model_validate(user).model_copy(
        update={"streak_days": displayed_streak(user.last_activity_date, today, user.streak_days)}
    )


def update_user_track(db: Session, user: User, track: Track) -> User:
    """Save the learning area the user chose on the Choice page."""
    user.track = track.value
    db.commit()
    db.refresh(user)
    return user
