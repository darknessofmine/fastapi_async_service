from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from . import schemas
from core.models import Post


async def create_post(session: AsyncSession,
                      post_in: schemas.PostCreate) -> Post | None:
    post = Post(**post_in.model_dump())
    session.add(Post)
    await session.commit()
    return post


async def get_posts_with_authors(session: AsyncSession) -> Sequence[Post]:
    stmt = (
        select(Post)
        .options(joinedload(Post.user))
        .order_by(Post.id)
    )
    return await session.scalars(stmt)


async def get_post_by_id_with_author(session: AsyncSession,
                                     post_id: int) -> Post | None:
    return await session.scalar(
        select(Post)
        .where(Post.id == post_id)
        .options(joinedload(Post.user))
    )


async def update_post(session: AsyncSession,
                      post: Post,
                      post_update: schemas.PostUpdate) -> Post:
    for key, value in post_update.model_dump().items():
        setattr(post, key, value)
    await session.commit()
    return post


async def update_post_partial(session: AsyncSession,
                              post: Post,
                              post_update: schemas.PostUpdatePartial) -> Post:
    for key, value in post_update.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    await session.commit()
    return post


async def delete_post(session: AsyncSession,
                      post: Post) -> None:
    await session.delete(post)
    await session.commit()