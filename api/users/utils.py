from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from api.auth import utils as auth_utils
from core.db_helper import db_helper
from core.models import User


async def _get_user_or_404(
    username: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
    with_posts: bool = False,
) -> User:
    if with_posts:
        user = await crud.get_user_by_username_with_posts(
            session=session,
            username=username,
        )
    else:
        user = await crud.get_user_by_username(
            session=session,
            username=username,
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found!",
        )
    return user


async def get_user_by_username_or_404(
    username: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user = await _get_user_or_404(username=username, session=session)
    return user


async def get_user_with_posts_by_username_or_404(
    username: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user = await _get_user_or_404(
        username=username,
        session=session,
        with_posts=True,
    )
    return user


async def get_author_by_id_with_sub_tiers_or_404(
    author_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user = await crud.get_user_by_id_with_sub_tiers(
        user_id=author_id,
        session=session,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user


async def get_user_by_id_or_404(
    user_id: int,
    session: AsyncSession
) -> User:
    user = await crud.get_user_by_id_with_sub_tiers(
        user_id=user_id,
        session=session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found!",
        )
    return user


def user_is_curr_user_or_403(payload: dict, user: User) -> None:
    current_user_id = payload.get("id")
    if current_user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("You can't change this user's profile!"),
        )


async def get_user_with_sub_tiers_or_404(
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}. Expected: access.",
        )
    user_id = payload.get("id")
    user = await crud.get_user_by_id_with_sub_tiers(
        user_id=user_id,
        session=session,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found!",
        )
    return user
