from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from core.models import Post, User


class Comment(Base):
    __tablename__ = "comments"

    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    created: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc),
        server_default=datetime.now(timezone.utc),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship()
