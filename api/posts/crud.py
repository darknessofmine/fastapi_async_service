from sqlalchemy import select, Sequence, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .schemas import PostCreate, PostUpdate, PostUpdatePartial
from core.models import Post


async def create_post(session: AsyncSession,
                      post_in: PostCreate,
                      author_id: int) -> Post | None:
    post_dict = post_in.model_dump()
    post_dict["user_id"] = author_id
    post = Post(**post_dict)
    session.add(post)
    await session.commit()
    return post


async def get_post_by_id(session: AsyncSession,
                         post_id: int) -> Post | None:
    return await session.scalar(
        select(Post)
        .where(Post.id == post_id)
        .options(
            joinedload(Post.user)
        )
    )


async def get_posts_with_authors(session: AsyncSession) -> Sequence[Post]:
    return await session.scalars(
        select(Post)
        .options(joinedload(Post.user))
        .order_by(Post.id)
    )


async def get_post_by_id_and_username_with_author(
        session: AsyncSession,
        post_id: int,
        username: str
) -> Post | None:
    return await session.scalar(
        select(Post)
        .where(and_(
            Post.user.has(username=username),
            (Post.id == post_id)
        )).options(
            joinedload(Post.user),
            joinedload(Post.comments)
        )
    )


async def get_post_by_id_and_username(
        session: AsyncSession,
        post_id: int,
        username: str
) -> Post | None:
    return await session.scalar(
        select(Post)
        .where(
            and_(Post.user.has(username=username),
                 Post.id == post_id)
        ).options(
            joinedload(Post.user)
        )
    )


async def update_post(session: AsyncSession,
                      post: Post,
                      post_update: PostUpdate | PostUpdatePartial,
                      partial: bool = False) -> Post:
    for key, value in post_update.model_dump(exclude_unset=partial).items():
        setattr(post, key, value)
    await session.commit()
    return post


async def update_post_tier(session: AsyncSession,
                           post: Post,
                           sub_tier_id: int) -> Post:
    setattr(post, "sub_tier_id", sub_tier_id)
    await session.commit()
    return post


async def delete_post(session: AsyncSession,
                      post: Post) -> None:
    await session.delete(post)
    await session.commit()
