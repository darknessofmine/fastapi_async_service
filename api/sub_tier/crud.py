from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from core.models import SubTier


async def create_sub_tier(sub_tier_in: schemas.SubTierCreate,
                          user_id: int,
                          session: AsyncSession) -> SubTier:
    sub_tier_dict = sub_tier_in.model_dump()
    sub_tier_dict["user_id"] = user_id
    sub_tier = SubTier(**sub_tier_dict)
    session.add(sub_tier)
    await session.commit()
    return sub_tier


async def get_sub_tier(sub_tier_id: int,
                       session: AsyncSession) -> SubTier | None:
    return await session.scalar(
        select(SubTier)
        .where(SubTier.id == sub_tier_id)
    )


async def update_sub_tier(sub_tier_update: schemas.SubTierUpdate,
                          sub_tier: SubTier,
                          session: AsyncSession) -> SubTier:
    for key, value in sub_tier_update.model_dump().items():
        setattr(sub_tier, key, value)
    await session.commit()
    return sub_tier


async def delete_sub_tier(sub_tier: SubTier, session: AsyncSession) -> None:
    await session.delete(sub_tier)
    await session.commit()
