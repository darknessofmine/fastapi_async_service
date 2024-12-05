from fastapi import APIRouter, Depends

from . import utils as auth_utils
from .jwt import utils as jwt_utils
from .jwt.schemas import TokenInfo
from api.users import schemas


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
def auth_login():
    ...


@router.post("/login", response_model=TokenInfo)
def auth_login_get_jwt(
    user: schemas.UserLogin = Depends(auth_utils.validate_auth_user),
):
    jwt_payload = {
        "sub":  user.username,
        "id": user.id
    }
    token = jwt_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/logout")
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
