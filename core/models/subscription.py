from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint(),
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sub_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
