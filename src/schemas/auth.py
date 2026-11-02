from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordData(BaseModel):
    """Payload asking for a password reset link."""

    email: EmailStr


class ResetPasswordData(BaseModel):
    """Payload setting a new password with the token from a reset link."""

    token: str
    password: str = Field(..., min_length=6, max_length=32, description="New password")


class LoginData(BaseModel):
    """Payload for user authentication."""

    username_or_email: str = Field(
        ...,
        description="Username or email address",
        examples=["john_doe", "john@example.com"],
    )
    password: str = Field(
        ..., min_length=1, max_length=32, description="Account password", examples=["secret123"]
    )


class Token(BaseModel):
    """Bearer token response payload."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Decoded JWT payload structure."""

    sub: str | None = None
    exp: int | None = None
