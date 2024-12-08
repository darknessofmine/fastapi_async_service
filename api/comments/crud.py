from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .import schemas
from core.db_helper import db_helper
from core.models import Comment


async def create_comment(
        comment_in: schemas.CommentCreate,
        user_id: int,
        post_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> Comment:
    comment_dict = comment_in.model_dump()
    comment_dict["user_id"] = user_id
    comment_dict["post_id"] = post_id
    new_comment = Comment(**comment_dict)
    session.add(new_comment)
    await session.commit()
    return new_comment
