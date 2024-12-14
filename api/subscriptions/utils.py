from typing import Annotated

from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from api.auth import utils as auth_utils
from core.db_helper import db_helper
from core.models import Subscription


async def get_subscription(
    author_id: Annotated[int, Path],
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Subscription | None:
    user_id = payload.get("id")
    return await crud.get_subscription(
        author_id=author_id,
        user_id=user_id,
        session=session,
    )


def user_is_not_author_or_403(author_id: int, user_id: int) -> None:
    if author_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't sub/unsub yourself!",
        )
