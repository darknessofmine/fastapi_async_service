from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class SubTier(Base):
    __tablename__ = "sub_tiers"

    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
