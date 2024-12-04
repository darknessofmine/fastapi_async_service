from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.db_helper import db_helper


router = APIRouter(tags=["subscription"])


@router.post("/{user_id}/subscribe")
async def subscribe(
    user_id: int,
    sub_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    is_subscribed = await crud.get_subscription(
        author_id=user_id,
        sub_id=sub_id,
        session=session,
    )
    if is_subscribed is None:
        return await crud.subscribe(
            author_id=user_id,
            sub_id=sub_id,
            session=session,
        )
    return {
        "message": "You are alrealy subscribed! You can't do it twice!"
    }


@router.post("/{user_id}/unsub")
async def unsub(
    user_id: int,
    sub_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    subscription = await crud.get_subscription(
        author_id=user_id,
        sub_id=sub_id,
        session=session,
    )
    if subscription is not None:
        return await crud.delete_subscription(
            subscription=subscription,
            session=session,
        )
    return {
        "message": "You are not subscribed!"
    }
