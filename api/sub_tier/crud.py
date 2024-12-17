from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import SubTierCreate, SubTierUpdate, SubTierUpdatePartial
from core.models import SubTier


async def create_sub_tier(sub_tier_in: SubTierCreate,
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


async def get_sub_tiers_by_username(
    username: str,
    session: AsyncSession,
) -> Sequence[SubTier] | None:
    return await session.scalars(
        select(SubTier)
        .where(
            SubTier.user.has(username=username)
        )
        .order_by(SubTier.price)
    )


async def update_sub_tier(sub_tier_upd: SubTierUpdate | SubTierUpdatePartial,
                          sub_tier: SubTier,
                          session: AsyncSession,
                          partial: bool = False) -> SubTier:
    for key, value in sub_tier_upd.model_dump(exclude_unset=partial).items():
        setattr(sub_tier, key, value)
    await session.commit()
    return sub_tier


async def delete_sub_tier(sub_tier: SubTier, session: AsyncSession) -> None:
    await session.delete(sub_tier)
    await session.commit()
