from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tag(Base):
    __talbename__ = "tags"

    text: Mapped[str] = mapped_column(String(50), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
