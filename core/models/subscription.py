from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from core.models import SubTier, User


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint(
            "author_id", "sub_id",
            name="unique_author_sub"
        ),
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sub_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(
        "User",
        back_populates="subscriptions",
        foreign_keys=[author_id],
        lazy="joined",
    )
    sub: Mapped["User"] = relationship(
        "User",
        back_populates="subscribers",
        foreign_keys=[sub_id],
        lazy="joined",
    )
    sub_tier: Mapped["SubTier"] | None = relationship(
        back_populates="subscription",
    )
