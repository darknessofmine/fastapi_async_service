from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import utils as sub_utils
from api.auth import utils as auth_utils
from api.sub_tier import utils as sub_tier_utils
from api.users import utils as user_utils
from core.db_helper import db_helper
from core.models import Subscription, User


router = APIRouter(tags=["subscription"])


@router.post("/{author_id}/subscribe",
             status_code=status.HTTP_200_OK)
async def subscribe(
    sub_tier_id: int = Form(),
    author: User = Depends(user_utils.get_author_by_id_with_sub_tiers_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
    subscription: Subscription = Depends(sub_utils.get_subscription),
):
    sub_tier_utils.author_owns_chosen_sub_tier_or_404(
        sub_tiers=author.sub_tiers,
        sub_tier_id=sub_tier_id,
    )
    user_id = payload.get("id")
    sub_utils.user_is_not_author_or_403(author_id=author.id, user_id=user_id)
    if subscription is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are already subscribed!",
        )
    return await crud.subscribe(
        author_id=author.id,
        user_id=user_id,
        sub_tier_id=sub_tier_id,
        session=session,
    )


@router.post("/{author_id}/unsubscribe", status_code=status.HTTP_200_OK)
async def unsub(
    author: User = Depends(user_utils.get_author_by_id_with_sub_tiers_or_404),
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
    subscription: Subscription = Depends(sub_utils.get_subscription),
):
    user_id = payload.get("id")
    sub_utils.user_is_not_author_or_403(author_id=author.id, user_id=user_id)
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not subscribed!",
        )
    await crud.delete_subscription(
        subscription=subscription,
        session=session,
    )
    return {"message": "You have successfully unsubscribed!"}


@router.patch("/{author_id}/subscribe/change-tier",
              status_code=status.HTTP_200_OK)
async def change_subscription_tier(
    new_sub_tier_id: int,
    author: User = Depends(user_utils.get_author_by_id_with_sub_tiers_or_404),
    user: User = Depends(auth_utils.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
    subscription: Subscription = Depends(sub_utils.get_subscription)
):
    sub_tier_utils.author_owns_chosen_sub_tier_or_404(
        sub_tiers=author.sub_tiers,
        sub_tier_id=new_sub_tier_id,
    )
    sub_utils.user_is_not_author_or_403(author_id=author.id, user_id=user.id)
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("To change your subscription level, "
                    "you need to subscribe first!"),
        )
    return await crud.change_subscription_tier(
        new_sub_tier_id=new_sub_tier_id,
        subscription=subscription,
        session=session,
    )
