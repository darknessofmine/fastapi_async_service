from typing import Annotated, Any

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper


def get_object_by_id(obj_type: Any):
    async def func(
            id: Annotated[int, Path],
            session: AsyncSession = Depends(db_helper.session_dependency),
    ) -> Any:
        obj = await session.get(obj_type, id)
        if obj is not None:
            return obj
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{obj_type.__name__} with id {id} not found!"
        )
    return func
