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
    password: str


class UserUpdate(UserCreate):
    ...


class UserUpdatePartial(UserUpdate):
    username: str | None = None
    password: str | None = None


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
