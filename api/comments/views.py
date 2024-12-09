from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from . import crud
from api.auth import utils as auth_utils
from api.posts import utils as post_utils
from core.db_helper import db_helper
from core.models import Post

router = APIRouter(tags=["comments"])


@router.post(
    "/{username}/{post_id}/comment/create",
    response_model=schemas.CommentResponse,
)
async def create_comment(
    comment_in: schemas.CommentCreate,
    post: Post = Depends(post_utils.get_post_by_id_and_username),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = payload.get("id")
    return await crud.create_comment(
        comment_in=comment_in,
        user_id=user_id,
        post_id=post.id,
        session=session,
    )


@router.patch("/{username}/{post_id}/comment/{comment_id}/update")
async def update_comment(
    comment_id: int,
    comment_in: schemas.CommentUpdate,
    post: Post = Depends(post_utils.get_post_by_id_and_username),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    comment = await crud.get_comment(comment_id=comment_id, session=session)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Comment not found."
                    "Please make sure url you're using is correct.")
        )
    user_id = payload.get("id")
    if user_id != comment.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("Comment can be change only by its author."),
        )
    return await crud.update_comment(
        comment_in=comment_in,
        comment=comment,
        session=session,
    )
