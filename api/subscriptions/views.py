from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from api.auth import utils as auth_utils
from core.db_helper import db_helper


router = APIRouter(tags=["subscription"])


@router.post("/{author_id}/subscribe")
async def subscribe(
    author_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = payload.get("id")
    if user_id == author_id:
        return {
            "message": "You can't subscribe yourself!"
        }
    is_subscribed = await crud.get_subscription(
        author_id=author_id,
        sub_id=user_id,
        session=session,
    )
    if is_subscribed is None:
        return await crud.subscribe(
            author_id=author_id,
            sub_id=user_id,
            session=session,
        )
    return {
        "message": "You are alrealy subscribed! You can't do it twice!"
    }


@router.post("/{author_id}/unsub")
async def unsub(
    author_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = payload.get("id")
    subscription = await crud.get_subscription(
        author_id=author_id,
        sub_id=user_id,
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
