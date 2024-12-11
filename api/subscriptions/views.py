from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import utils as sub_utils
from api.auth import utils as auth_utils
from core.db_helper import db_helper
from core.models import Subscription


router = APIRouter(tags=["subscription"])


@router.post("/{author_id}/subscribe", status_code=status.HTTP_200_OK)
async def subscribe(
    author_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
    subscription: Subscription = Depends(sub_utils.get_subscription),
):
    user_id = payload.get("id")
    sub_utils.user_is_not_author_or_403(author_id=author_id, user_id=user_id)
    if subscription is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are already subscribed!",
        )
    return await crud.subscribe(
        author_id=author_id,
        user_id=user_id,
        session=session,
    )


@router.post("/{author_id}/unsub", status_code=status.HTTP_200_OK)
async def unsub(
    author_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
    subscription: Subscription = Depends(sub_utils.get_subscription),
):
    user_id = payload.get("id")
    sub_utils.user_is_not_author_or_403(author_id=author_id, user_id=user_id)
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not subscribed!",
        )
    await crud.delete_subscription(
        subscription=subscription,
        session=session,
    )
