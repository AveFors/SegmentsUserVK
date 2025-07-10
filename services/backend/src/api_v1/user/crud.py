from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, func

from core.models import UserSegment
from core.models.user import User
from api_v1.user.schemas import UserCreateSchema, UserSchema, UserBaseSchema, UserUpdateSchema


async def get_all_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()

    user_schemas = [UserSchema.model_validate(user) for user in users]

    return user_schemas


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def user_create(session: AsyncSession, user_in: UserCreateSchema) -> User:
    user = User(**user_in.model_dump())
    stmt = (
        select(func.count())
        .select_from(User)
        .where(User.email == user_in.email)
    )
    user_exists = await session.scalar(stmt)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    session.add(user)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    if user:
        await session.delete(user)
        await session.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )


async def update_user(user_in: UserUpdateSchema, session: AsyncSession, user: User) -> UserSchema:
    update_data = user_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if value == "string":
            continue
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)

    return UserSchema.model_validate(user)



async def get_users_by_segment(session: AsyncSession, segment_id: int) -> list[UserSchema]:
    stmt = (
        select(User)
        .join(UserSegment, User.id == UserSegment.user_id)
        .where(UserSegment.segment_id == segment_id)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()

    user_schemas = [UserSchema.model_validate(user) for user in users]

    return user_schemas