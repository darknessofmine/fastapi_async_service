from fastapi import APIRouter, Depends

from . import utils as auth_utils
from .jwt.schemas import TokenInfo
from api.users import schemas


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(auth_utils.http_bearer)],
)


@router.post("/login", response_model=TokenInfo)
def auth_login_get_jwt(
    user: schemas.UserLogin = Depends(auth_utils.validate_auth_user),
):
    access_token = auth_utils.create_access_token(user=user)
    refresh_token = auth_utils.create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/logout")
def auth_logout():
    ...


@router.get("/me")
def auth_get_current_user(
    user: schemas.UserResponse = Depends(auth_utils.get_current_user),
):
    return {
        "id": user.id,
        "username": user.username,
    }


@router.post(
        "/refresh-jwt",
        response_model=TokenInfo,
        response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: schemas.UserLogin = Depends(auth_utils.get_current_user_for_refresh),
):
    access_token = auth_utils.create_access_token(user=user)
    return TokenInfo(
        access_token=access_token
    )
