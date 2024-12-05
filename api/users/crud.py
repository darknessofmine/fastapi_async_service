from sqlalchemy import select, Sequence
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from core.models import User


async def create_user(session: AsyncSession,
                      user_in: schemas.UserCreate) -> User | None:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession,
                               username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return await session.scalar(stmt)


async def get_user_by_id(session: AsyncSession,
                         user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return await session.scalar(stmt)


async def get_users_with_posts(session: AsyncSession) -> Sequence[User]:
    stmt = (
        select(User)
        .options(selectinload(User.posts))
        .order_by(User.id)
    )
    return await session.scalars(stmt)


async def get_user_by_id_with_posts(session: AsyncSession,
                                    user_id: int) -> User | None:
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(joinedload(User.posts))
    )
    return await session.scalar(stmt)


async def get_user_by_username_with_posts(session: AsyncSession,
                                          username: str) -> User | None:
    stmt = (
        select(User)
        .where(User.username == username)
        .options(joinedload(User.posts))
    )
    return await session.scalar(stmt)


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
