from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import utils as auth_utils
from api.posts import crud
from api.posts import utils as post_utils
from api.posts import schemas
from core.db_helper import db_helper
from core.models import Post


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
    post: Post = Depends(post_utils.get_post_by_id_and_username),
):
    return post


@router.put("/posts/{post_id}")
async def update_post(
    post_in: schemas.PostUpdate,
    post: Post = Depends(post_utils.get_post_by_id),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    post_utils.user_is_author_or_403(post=post, payload=payload)
    return await crud.update_post(
        post=post,
        post_update=post_in,
        session=session,
    )


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Post = Depends(post_utils.get_post_by_id),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    username = payload.get("sub")
    if post.user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post can be deleted only by its author."
        )
    return await crud.delete_post(
        post=post,
        session=session,
    )
