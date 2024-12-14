from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import schemas
from api.auth import utils as auth_utils
from core.db_helper import db_helper


router = APIRouter(tags=["sub_tiers"])


@router.post("/subscription/create",
             response_model=schemas.SubTierResponse,
             status_code=status.HTTP_201_CREATED)
async def create_sub_tier(
    sub_tier_in: schemas.SubTierCreate,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    user_id = payload.get("id")
    return await crud.create_sub_tier(
        sub_tier_in=sub_tier_in,
        user_id=user_id,
        session=session,
    )
