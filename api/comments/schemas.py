from datetime import datetime
# from typing import TYPE_CHECKING

from pydantic import BaseModel


# if TYPE_CHECKING:
#     from api.users.schemas import UserResponse


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    ...


class CommentUpdate(CommentCreate):
    ...


class CommentResponse(CommentBase):
    id: int
    # user: UserResponse
    created: datetime
