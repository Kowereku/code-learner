from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.model.db import Base


class UserCodeSolution(Base):
    """A code exercise the user solved by typing; each exercise counts once towards "Own code"."""

    __tablename__ = "user_code_solutions"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
    )
    solved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
