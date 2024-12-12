from datetime import timedelta

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from .jwt import utils as jwt_utils
from api.users import crud
from api.users import schemas
from core.config import settings
from core.db_helper import db_helper
from core.models import User


http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> User:
    user = await crud.get_user_by_username_with_password(
        session=session,
        username=username,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password!",
        )

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
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}. Expected: access.",
        )

    user_id = payload.get("id")
    user = await crud.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found!",
        )
    return user


async def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> User:
    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}. Expected: refresh.",
        )

    username = payload.get("sub")
    user = await crud.get_user_by_username_with_password(
        session=session,
        username=username,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found!",
        )
    return user


def create_jwt_token(
    token_info: dict,
    token_type: str,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelda: timedelta | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_info)
    return jwt_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelda=expire_timedelda,
    )


def create_access_token(
    user: schemas.UserLogin = Depends(validate_auth_user),
) -> str:
    jwt_payload = {
        "sub": user.username,
        "id": user.id
    }
    return create_jwt_token(
        token_info=jwt_payload,
        token_type="access",
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(
    user: schemas.UserLogin = Depends(validate_auth_user),
) -> str:
    jwt_payload = {"sub": user.username}
    return create_jwt_token(
        token_info=jwt_payload,
        token_type="refresh",
        expire_timedelda=settings.auth_jwt.refresh_token_expire_days,
    )
