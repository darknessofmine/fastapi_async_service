from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import utils as user_utils
from .schemas import UserCreate, UserUpdate, UserUpdatePartial
from api.auth import utils as auth_utils
from core.db_helper import db_helper
from core.models import User


router = APIRouter(tags=["users"])


@router.post("/",
             response_model=UserCreate,
             status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    new_user = await crud.create_user(session=session, user_in=user)
    return new_user


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_multiple(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    users = await crud.get_users_with_posts(session=session)
    return users.all()


@router.get("/subscriptions")
async def get_all_users_subscribed(
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = payload.get("id")
    users = await crud.get_all_users_subbed_with_posts(
        user_id=user_id,
        session=session,
    )
    return users.all()


@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_user_by_username(
    user: User = Depends(user_utils.get_user_with_posts_by_username_or_404),
):
    return user


@router.get("/subscriptions/available")
async def get_all_users_subbed_wit_posts_available(
    user: User = Depends(auth_utils.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    users = await crud.get_users_with_posts_available(
        user_id=user.id,
        session=session,
    )
    return users.unique().all()


@router.put("/{username}", status_code=status.HTTP_200_OK)
async def update_user(
    username: str,
    user_update: UserUpdate,
    user: User = Depends(user_utils.get_user_by_username_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """DELETE `USERNAME` FROM FUNCTION PARAMS"""
    user_utils.user_is_curr_user_or_403(user=user, payload=payload)
    return await crud.update_user(
        user=user,
        user_update=user_update,
        session=session,
    )


@router.patch("/{username}", status_code=status.HTTP_200_OK)
async def update_user_partial(
    username: str,
    user_update: UserUpdatePartial,
    user: User = Depends(user_utils.get_user_by_username_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """DELETE `USERNAME` FROM FUNCTION PARAMS"""
    user_utils.user_is_curr_user_or_403(user=user, payload=payload)
    return await crud.update_user(
        user=user,
        user_update=user_update,
        session=session,
        partial=True,
    )


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str,
    user: User = Depends(user_utils.get_user_by_username_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """DELETE `USERNAME` FROM FUNCTION PARAMS"""
    user_utils.user_is_curr_user_or_403(user=user, payload=payload)
    await crud.delete_user(user=user, session=session)
