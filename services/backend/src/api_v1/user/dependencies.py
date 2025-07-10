from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_user
from core.models import db_helper, User
from .schemas import UserSchema


async def get_user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await get_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
