import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

logger = logging.getLogger(__name__)

RESET_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an existing bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Generate a signed JWT token containing given payload data."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token string.

    Raises jwt.PyJWTError subclasses on invalid or expired token.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def create_reset_token(user_id: int, password_hash: str) -> str:
    """Token for a password reset link, valid for an hour.

    It is signed with the current password hash, so it stops working once the password changes
    and can never pass as an access token.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY + password_hash, algorithm=ALGORITHM)


def reset_token_user_id(token: str) -> int:
    """The user a reset token claims to be for; only trusted after check_reset_token."""
    return int(jwt.decode(token, options={"verify_signature": False})["sub"])


def check_reset_token(token: str, password_hash: str) -> None:
    """Raise jwt.PyJWTError unless the token is unexpired and was made for this password hash."""
    jwt.decode(token, SECRET_KEY + password_hash, algorithms=[ALGORITHM])
