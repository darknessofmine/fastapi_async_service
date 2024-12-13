from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


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
    price: Mapped[int] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id")
    )
