from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import schemas
from api.auth import utils as auth_utils
from api.posts import utils as post_utils
from api.sub_tier import utils as sub_tier_utils
from api.users import utils as user_utils
from core.db_helper import db_helper
from core.models import Post, User


router = APIRouter(tags=["posts"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
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


@router.get("/{username}/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(
    post: Post = Depends(post_utils.get_post_by_id_and_username),
):
    return post


@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
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


@router.patch("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post_partial(
    post_in: schemas.PostUpdatePartial,
    post: Post = Depends(post_utils.get_post_by_id),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    post_utils.user_is_author_or_403(post=post, payload=payload)
    return await crud.update_post(
        post=post,
        post_update=post_in,
        session=session,
        partial=True,
    )


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Post = Depends(post_utils.get_post_by_id),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    post_utils.user_is_author_or_403(post=post, payload=payload)
    await crud.delete_post(post=post, session=session)


@router.patch("/posts/{post_id}/update-tier",
              response_model=schemas.PostResponse,
              status_code=status.HTTP_200_OK)
async def update_post_tier(
    sub_tier_id: int = Form(),
    post: Post = Depends(post_utils.get_post_by_id),
    user: User = Depends(user_utils.get_user_with_sub_tiers_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    post_utils.user_is_author_or_403(post=post, payload=payload)
    sub_tier_utils.author_owns_chosen_sub_tier_or_404(
        sub_tiers=user.sub_tiers,
        sub_tier_id=sub_tier_id,
    )
    return await crud.update_post_tier(
        post=post,
        sub_tier_id=sub_tier_id,
        session=session
    )
