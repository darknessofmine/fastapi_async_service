from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Subscription


async def is_subscribed(author_id: int,
                        sub_id: int,
                        session: AsyncSession) -> Subscription:
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


async def unsub(subscription: Subscription,
                session: AsyncSession) -> None:
    await session.delete(subscription)
    await session.commit()
