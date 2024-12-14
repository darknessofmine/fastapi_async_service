from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.db_helper import db_helper
from core.models import SubTier


async def get_sub_tier_or_404(
    sub_tier_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> SubTier:
    sub_tier = await crud.get_sub_tier(
        sub_tier_id=sub_tier_id,
        session=session,
    )
    if sub_tier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subsctription tier not found!",
        )
    return sub_tier


def user_is_author_or_403(payload: dict, sub_tier: SubTier) -> None:
    user_id = payload.get("id")
    if user_id != sub_tier.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("Subscription tier can be changed/deleted "
                    "only by its author."),
        )
