from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from core.models import Post, User


class Comment(Base):
    __tablename__ = "comments"

    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    created: Mapped[datetime] = mapped_column(server_default=now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), deferred=True)

    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship(back_populates="comments")
