from sqlalchemy import select, Sequence
from sqlalchemy.orm import joinedload, load_only, selectinload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, UserUpdate, UserUpdatePartial
from core.models import Post, Subscription, User


async def create_user(session: AsyncSession,
                      user_in: UserCreate) -> User | None:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession,
                               username: str) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.username == username)
    )


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
                      user_update: UserUpdate | UserUpdatePartial,
                      partial: bool = False) -> User:
    for key, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession,
                      user: User) -> None:
    await session.delete(user)
    await session.commit()


async def get_all_users_subbed_with_posts(
    user_id: int,
    session: AsyncSession,
) -> Sequence[User]:
    return await session.scalars(
        select(User)
        .where(User.subscribers.any(sub_id=user_id))
        .options(
            selectinload(User.posts)
            .options(
                selectinload(Post.comments)
            )
        )
    )


async def get_user_by_id_with_sub_tiers(
    user_id: int,
    session: AsyncSession,
) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.id == user_id)
        .options(
            joinedload(User.sub_tiers)
        )
    )


async def get_users_with_posts_available(
    user_id: int,
    session: AsyncSession,
) -> Sequence[User] | None:
    return await session.scalars(
        select(Subscription)
        .where(
            Subscription.sub_id == user_id
        )
        .join(Subscription.author)
        .options(contains_eager(
            Subscription.author,
        ))
        .join(User.posts)
        .options(contains_eager(
            Subscription.author,
            User.posts,
        ))
        .outerjoin(Post.comments)
        .options(contains_eager(
            Subscription.author,
            User.posts,
            Post.comments,
        ))
        .filter(
            Post.sub_tier_id == Subscription.sub_tier_id
        )
    )
