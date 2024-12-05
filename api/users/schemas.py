from pydantic import BaseModel, ConfigDict

from api.posts import PostRelated


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    posts: list["PostRelated"]

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    ...


class UserUpdate(UserCreate):
    ...


class UserLogin(UserBase):
    passworld: str
