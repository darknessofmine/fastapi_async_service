from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import User, UserCreate, UserUpdate
from api.utils import get_object_by_id
from core import models
from core.db_helper import db_helper


router = APIRouter(tags=["users"])


@router.post("/", response_model=UserCreate)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    new_user = await crud.create_user(session=session, user_in=user)
    return new_user


@router.get("/{username}", response_model=User)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await crud.get_user_by_username_with_posts(
        session=session,
        username=username,
    )
    if user is not None:
        return user
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found!"
        )


@router.get("/", response_model=list[User])
async def get_users_multiple(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_users_with_posts(session=session)


@router.put("/{username}")
async def update_user(
    username: str,
    user_update: UserUpdate,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await crud.get_user_by_username(
        username=username,
        session=session,
    )
    return await crud.update_user(
        user=user,
        user_update=user_update,
        session=session,
    )


@router.delete("/{user_id}")
async def delete_user(
    user: User = Depends(get_object_by_id(model=models.User)),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.delete_user(user=user, session=session)
