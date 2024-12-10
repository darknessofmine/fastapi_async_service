from sqlalchemy import select, Sequence
from sqlalchemy.orm import joinedload, load_only, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from core.models import User, Post


async def create_user(session: AsyncSession,
                      user_in: schemas.UserCreate) -> User | None:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username_with_password(
    session: AsyncSession,
    username: str,
) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.username == username)
        .options(
            load_only(User.username, User.password)
        )
    )


async def get_user_by_id(session: AsyncSession,
                         user_id: int) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.id == user_id)
    )


async def get_users_with_posts(session: AsyncSession) -> Sequence[User]:
    return await session.scalars(
        select(User)
        .options(
            selectinload(User.posts)
            .selectinload(Post.comments)
        )
    )


async def get_user_by_id_with_posts(session: AsyncSession,
                                    user_id: int) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.id == user_id)
        .options(joinedload(User.posts))
    )


async def get_user_by_username_with_posts(session: AsyncSession,
                                          username: str) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.username == username)
        .options(
            joinedload(User.posts)
            .selectinload(Post.comments)
        )
    )


async def update_user(session: AsyncSession,
                      user: User,
                      user_update: schemas.UserUpdate) -> User:
    for key, value in user_update.model_dump().items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession,
                      user: User) -> None:
    await session.delete(user)
    await session.commit()
