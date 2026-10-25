from sqlalchemy import JSON, BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.db import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    track: Mapped[str | None] = mapped_column(String(50), nullable=True)
    xp_reward: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
    translations: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    modules: Mapped[list["Module"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.order_index",
    )
    user_links: Mapped[list["UserCourse"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
