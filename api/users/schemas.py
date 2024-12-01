from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from core.models import Post


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    posts: list["Post"] | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )
