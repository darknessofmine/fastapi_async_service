from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import schemas
from . import utils as sub_tier_utils
from api.auth import utils as auth_utils
from core.db_helper import db_helper
from core.models import SubTier


router = APIRouter(tags=["sub_tiers"])


@router.post("/subscription",
             response_model=schemas.SubTierResponse,
             status_code=status.HTTP_201_CREATED)
async def create_sub_tier(
    sub_tier_in: schemas.SubTierCreate,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = payload.get("id")
    return await crud.create_sub_tier(
        sub_tier_in=sub_tier_in,
        user_id=user_id,
        session=session,
    )


@router.put("/subscription/{sub_id}",
            response_model=schemas.SubTierResponse,
            status_code=status.HTTP_200_OK)
async def update_sub_tier(
    sub_tier_update: schemas.SubTierUpdate,
    sub_tier: SubTier = Depends(sub_tier_utils.get_sub_tier_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sub_tier_utils.user_is_author_or_403(payload=payload, sub_tier=sub_tier)
    return await crud.update_sub_tier(
        sub_tier_update=sub_tier_update,
        sub_tier=sub_tier,
        session=session,
    )


@router.delete("subscription/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_tier(
    sub_tier: SubTier = Depends(sub_tier_utils.get_sub_tier_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sub_tier_utils.user_is_author_or_403(payload=payload, sub_tier=sub_tier)
    await crud.delete_sub_tier(sub_tier=sub_tier, session=session)
