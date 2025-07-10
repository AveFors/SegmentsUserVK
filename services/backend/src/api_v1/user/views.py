from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models.db_helper import db_helper
from api_v1.user.schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from api_v1.user.dependencies import get_user_by_id
from api_v1.user import crud

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserSchema])
async def get_all_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await crud.get_all_users(session)
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user: User = Depends(get_user_by_id),
):
    return user


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreateSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user = await crud.user_create(session, user_in)
    return UserSchema.model_validate(user)


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_in: UserUpdateSchema,
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_user = await crud.update_user(user_in, session, user)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await crud.delete_user(session, user)
    return None
