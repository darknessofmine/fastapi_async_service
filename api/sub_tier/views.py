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
    return await sub_tier_utils.create_sub_tier_or_uq_constraint_exc(
        sub_tier_in=sub_tier_in,
        user_id=user_id,
        session=session
    )


@router.get("/subsciption/{username}",
            response_model=list[schemas.SubTierResponse],
            status_code=status.HTTP_200_OK)
async def get_sub_tiers_by_username(
    username: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sub_tiers = await crud.get_sub_tiers_by_username(
        username=username,
        session=session,
    )
    return sub_tiers.all()


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
    return await sub_tier_utils.update_sub_tier_or_uq_constraint_exc(
        sub_tier_upd=sub_tier_update,
        sub_tier=sub_tier,
        session=session,
    )


@router.patch("/subscription/{sub_id}",
              response_model=schemas.SubTierResponse,
              status_code=status.HTTP_200_OK)
async def update_sub_tier_partial(
    sub_tier_update: schemas.SubTierUpdatePartial,
    sub_tier: SubTier = Depends(sub_tier_utils.get_sub_tier_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sub_tier_utils.user_is_author_or_403(payload=payload, sub_tier=sub_tier)
    return await sub_tier_utils.update_sub_tier_or_uq_constraint_exc(
        sub_tier_upd=sub_tier_update,
        sub_tier=sub_tier,
        session=session,
        partial=True,
    )


@router.delete("subscription/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_tier(
    sub_tier: SubTier = Depends(sub_tier_utils.get_sub_tier_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sub_tier_utils.user_is_author_or_403(payload=payload, sub_tier=sub_tier)
    await crud.delete_sub_tier(sub_tier=sub_tier, session=session)
