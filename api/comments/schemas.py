from datetime import datetime

from pydantic import BaseModel

from api.users.schemas import UserResponse


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    ...


class CommentUpdate(CommentCreate):
    ...


class CommentResponse(CommentBase):
    id: int
    user: "UserResponse"
    created: datetime
