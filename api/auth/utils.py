from fastapi import Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.crud import get_user_by_username
from core.db_helper import db_helper


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!",
    )
    user = await get_user_by_username(session=session, username=username)
    if not user:
        raise unauthed_exc

    if user.password != password:
        raise unauthed_exc

    return user
