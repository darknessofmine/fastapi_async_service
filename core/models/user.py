from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .post import Post
    from .subscription import Subscription


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        deferred=True,
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    subscribers: Mapped[list["Subscription"] | None] = relationship(
        "Subscription",
        back_populates="author",
        foreign_keys="Subscription.author_id"
    )
    subscriptions: Mapped[list["Subscription"] | None] = relationship(
        "Subscription",
        back_populates="sub",
        foreign_keys="Subscription.sub_id"
    )
