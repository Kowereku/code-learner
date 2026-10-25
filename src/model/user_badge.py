from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.db import Base


class UserBadge(Base):
    """A badge a user has earned; the badge itself is defined in src/core/badges.py."""

    __tablename__ = "user_badges"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    badge_code: Mapped[str] = mapped_column(String(50), primary_key=True)
    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="badges")
