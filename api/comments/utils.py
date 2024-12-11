from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.db_helper import db_helper
from core.models import Comment


async def get_comment_or_404(
    comment_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Comment:
    comment = await crud.get_comment_by_id(
        comment_id=comment_id,
        session=session,
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Comment not found. "
                    "Please make sure url you're using is correct."),
        )
    return comment


def user_is_author_or_403(payload: dict, comment: Comment) -> None:
    user_id = payload.get("id")
    if user_id != comment.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("Comment can be changed/deleted only by its author."),
        )
