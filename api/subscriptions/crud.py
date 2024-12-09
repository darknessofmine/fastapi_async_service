from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Subscription


async def get_subscription(author_id: int,
                           sub_id: int,
                           session: AsyncSession) -> Subscription | None:
    return await session.scalar(
        select(Subscription)
        .where(
            Subscription.sub_id == sub_id
            and Subscription.author_id == author_id
        )
    )


async def subscribe(author_id: int,
                    sub_id: int,
                    session: AsyncSession) -> Subscription:
    subscription = Subscription(author_id=author_id, sub_id=sub_id)
    session.add(subscription)
    await session.commit()
    return subscription


async def delete_subscription(subscription: Subscription,
                              session: AsyncSession) -> None:
    await session.delete(subscription)
    await session.commit()
