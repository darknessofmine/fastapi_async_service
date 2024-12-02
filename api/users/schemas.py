from pydantic import BaseModel, ConfigDict

from ..posts.schemas import PostRelated


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    posts: list[PostRelated]

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    ...


class UserUpdate(UserCreate):
    ...
