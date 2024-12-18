from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from api.comments.schemas import CommentResponse

if TYPE_CHECKING:
    from api.users import User


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
    sub_tier_id: int | None = None


class PostUpdate(PostCreate):
    ...


class PostUpdatePartial(PostCreate):
    title: str | None = None
    text: str | None = None
    sub_tier_id: int | None = None


class PostRelated(PostBase):
    id: int
    comments: list["CommentResponse"]


class PostResponse(PostBase):
    user_id: int
    sub_tier_id: int
