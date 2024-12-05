from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils as auth_utils
from .jwt import utils as jwt_utils
from .jwt.schemas import TokenInfo
from api.users import schemas
from core.db_helper import db_helper


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
def auth_login():
    ...


@router.post("/login", response_model=TokenInfo)
def auth_login_get_jwt(
    user: schemas.UserLogin = Depends(auth_utils.validate_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    jwt_payload = {
        "sub": user.id,
        "username": user.username
    }
    token = jwt_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        asess_token=token,
        token_type="Bearer",
    )


@router.get("/logout")
def auth_logout():
    ...
