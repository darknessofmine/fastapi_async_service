from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from core.models import Comment, SubTier, User


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str | None] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"] | None] = relationship()
    sub_tier: Mapped["SubTier"] = relationship(back_populates="post")
