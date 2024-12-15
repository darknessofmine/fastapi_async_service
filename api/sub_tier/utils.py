from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import schemas
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


def author_owns_chosen_sub_tier_or_404(
    sub_tiers: list[SubTier],
    sub_tier_id: int,
) -> None:
    for sub_tier in sub_tiers:
        if sub_tier.id == sub_tier_id:
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User dosn't have this subscription.",
    )


async def create_sub_or_uq_constraint_exc(
    sub_tier_in: schemas.SubTierCreate,
    user_id: int,
    session: AsyncSession,
) -> SubTier:
    try:
        return await crud.create_sub_tier(
            sub_tier_in=sub_tier_in,
            user_id=user_id,
            session=session,
        )
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__["orig"]),
        )
