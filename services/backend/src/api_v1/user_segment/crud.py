from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from core.models.user_segment import UserSegment
from api_v1.user_segment.schemas import UserSegmentCreateSchema

async def add_user_to_segment(session: AsyncSession, data: UserSegmentCreateSchema) -> UserSegment:
    stmt = select(func.count()).select_from(UserSegment).where(
        UserSegment.user_id == data.user_id,
        UserSegment.segment_id == data.segment_id,
    )
    exists = await session.scalar(stmt)
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already in segment")

    new_entry = UserSegment(**data.model_dump())
    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)
    return new_entry

async def remove_user_from_segment(session: AsyncSession, user_id: int, segment_id: int):
    stmt = select(UserSegment).where(
        UserSegment.user_id == user_id,
        UserSegment.segment_id == segment_id,
    )
    result = await session.execute(stmt)
    user_segment = result.scalar_one_or_none()

    if not user_segment:
        raise HTTPException(status_code=404, detail="User not in segment")

    await session.delete(user_segment)
    await session.commit()
