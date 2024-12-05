from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from .jwt import utils as jwt_utils
from api.users.crud import get_user_by_id, get_user_by_username
from core.db_helper import db_helper
from core.models import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> User:
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


def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = jwt_utils.decode_jwt(token=token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token! {exc}"
        )
    return payload


async def get_current_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user_id = payload.get("id")
    user = await get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found!",
        )
    return user
