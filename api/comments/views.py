from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from . import crud
from api.auth import utils as auth_utils
from api.posts import utils as post_utils
from core.db_helper import db_helper
from core.models import Post

router = APIRouter(tags=["comments"])


@router.post(
    "/{username}/{post_id}/create",
    response_model=schemas.CommentResponse,
)
async def create_comment(
    comment_in: schemas.CommentCreate,
    post: Post = Depends(post_utils.get_post_by_id_and_username),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    user_id = payload.get("id")
    return await crud.create_comment(
        comment_in=comment_in,
        user_id=user_id,
        post_id=post.id,
        session=session,
    )
