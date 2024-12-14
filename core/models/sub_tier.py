from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

if TYPE_CHECKING:
    from core.models import Post, Subscription, User


class SubTier(Base):
    __tablename__ = "sub_tiers"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "title",
            name="unique_title_user_id",
        ),
    )

    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[str] = mapped_column(String(500))
    price: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id"),
    )

    user: Mapped["User"] = relationship(back_populates="sub_tiers")
    post: Mapped["Post"] = relationship(back_populates="sub_tier")
    subscription: Mapped["Subscription"] = relationship(
        back_populates="sub_tier",
    )
