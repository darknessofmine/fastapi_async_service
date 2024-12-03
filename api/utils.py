from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Base


def get_object_by_id(model: Base):
    async def func(
            id: Annotated[int, Path],
            session: AsyncSession = Depends(db_helper.session_dependency),
    ) -> Base:
        obj = await session.get(model, id)
        if obj is not None:
            return obj
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} with id {id} not found!"
        )
    return func
