from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .import schemas
from core.models import Comment


async def create_comment(comment_in: schemas.CommentCreate,
                         user_id: int,
                         post_id: int,
                         session: AsyncSession) -> Comment:
    comment_dict = comment_in.model_dump()
    comment_dict["user_id"] = user_id
    comment_dict["post_id"] = post_id
    new_comment = Comment(**comment_dict)
    session.add(new_comment)
    await session.commit()
    return new_comment


async def get_comment_by_id(comment_id: int,
                            session: AsyncSession) -> Comment:
    return await session.scalar(
        select(Comment)
        .add_columns(Comment.user_id)
        .where(Comment.id == comment_id)
    )


async def update_comment(comment_in: schemas.CommentUpdate,
                         comment: Comment,
                         session: AsyncSession) -> Comment:
    for key, value in comment_in.model_dump().items():
        setattr(comment, key, value)
    await session.commit()
    return comment


async def delete_comment(comment: Comment,
                         session: AsyncSession) -> None:
    await session.delete(comment)
    await session.commit()
