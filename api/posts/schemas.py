from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from core.models import User


class PostBase(BaseModel):
    title: str
    text: str


class Post(PostBase):
    id: int
    user: "User"

    model_config = ConfigDict(
        from_attributes=True,
    )


class PostCreate(PostBase):
    ...


class PostUpdate(PostCreate):
    ...


class PostUpdatePartial(PostCreate):
    title: str | None = None
    text: str | None = None


class PostRelated(PostBase):
    id: int
