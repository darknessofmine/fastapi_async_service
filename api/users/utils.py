from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
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


def user_is_curr_user_or_403(payload: dict, user: User) -> None:
    current_user_id = payload.get("id")
    if current_user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("You can't change this users profile!"),
        )
