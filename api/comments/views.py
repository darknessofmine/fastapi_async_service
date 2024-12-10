from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from . import crud
from . import utils as comment_utils
from api.auth import utils as auth_utils
from api.posts import utils as post_utils
from core.db_helper import db_helper
from core.models import Comment, Post

router = APIRouter(tags=["comments"])


@router.post(
    "/{username}/{post_id}/comments/create",
    response_model=schemas.CommentResponse,
    status_code=status.HTTP_201_CREATED,
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


@router.patch(
    "/comments/{comment_id}",
    response_model=schemas.CommentResponse,
)
async def update_comment(
    comment_in: schemas.CommentUpdate,
    comment: Comment = Depends(comment_utils.get_comment_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    comment_utils.user_is_author_or_403(payload=payload, comment=comment)
    return await crud.update_comment(
        comment_in=comment_in,
        comment=comment,
        session=session,
    )


@router.delete("comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment: Comment = Depends(comment_utils.get_comment_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    comment_utils.user_is_author_or_403(payload=payload, comment=comment)
    await crud.delete_comment(comment=comment, session=session)
