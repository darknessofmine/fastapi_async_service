from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import utils as auth_utils
from api.posts import crud
from api.posts import schemas as schemas
from core.db_helper import db_helper


router = APIRouter(tags=["posts"])


@router.post("/create")
async def create_post(
    post: schemas.PostCreate = Form(),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = payload.get("id")
    return await crud.create_post(
        session=session,
        post_in=post,
        author_id=user_id,
    )


@router.get("/{username}/{post_id}")
async def get_post(
    username: str,
    post_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    post = await crud.get_post_by_id_with_author(
        session=session,
        post_id=post_id,
        username=username
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found. Please make sure the url is correct."
        )
    return post
