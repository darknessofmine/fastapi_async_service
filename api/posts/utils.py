from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.db_helper import db_helper
from core.models import Post


async def get_post_by_id(
    post_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Post:
    post = await crud.get_post_by_id(post_id=post_id, session=session)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found."
        )
    return post


async def get_post_by_id_and_username(
    username: str = Annotated[str, Path],
    post_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Post:
    post = await crud.get_post_by_id_and_username(
        username=username,
        post_id=post_id,
        session=session,
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Post not found. Please make sure url you're using is correct."
            )
        )
    return post
