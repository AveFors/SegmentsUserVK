from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.models import UserSegment
from core.models.segment import Segment
from api_v1.segment.schemas import SegmentCreateSchema, SegmentUpdateSchema, SegmentSchema


async def get_all_segments(session: AsyncSession):
    stmt = select(Segment).order_by(Segment.id)
    result = await session.execute(stmt)
    segments = result.scalars().all()

    segment_schemas = [SegmentSchema.model_validate(segment) for segment in segments]

    return segment_schemas

async def get_segment(segment_id: int, session: AsyncSession) -> Segment | None:
    return await session.get(Segment, segment_id)

async def create_segment(session: AsyncSession, segment_in: SegmentCreateSchema) -> Segment:
    segment = Segment(**segment_in.model_dump())
    exists_stmt = select(func.count()).select_from(Segment).where(Segment.name == segment_in.name)
    exists = await session.scalar(exists_stmt)
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Segment with this name already exists")

    session.add(segment)
    await session.commit()
    await session.refresh(segment)
    return segment

async def update_segment(segment: Segment, segment_in: SegmentUpdateSchema, session: AsyncSession):
    update_data = segment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(segment, field, value)

    await session.commit()
    await session.refresh(segment)
    return segment

async def delete_segment(segment_id: int, session: AsyncSession):
    segment = await get_segment(segment_id, session)
    if not segment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found")
    await session.delete(segment)
    await session.commit()


async def get_segments_by_user(session: AsyncSession, user_id: int) -> list[SegmentSchema]:
    stmt = (
        select(Segment)
        .join(UserSegment, Segment.id == UserSegment.segment_id)
        .where(UserSegment.user_id == user_id)
    )
    result = await session.execute(stmt)
    segments = result.scalars().all()

    segment_schemas = [SegmentSchema.model_validate(segment) for segment in segments]

    return segment_schemas



from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from core.models.user_segment import UserSegment
from datetime import datetime
import math

async def assign_segment_to_percent(session: AsyncSession, segment_id: int, percent: float) -> list[int]:
    if not (0 < percent <= 100):
        raise ValueError("Percent must be between 0 and 100")

    subq = select(UserSegment.user_id).where(UserSegment.segment_id == segment_id)
    stmt = (
        select(User)
        .where(User.id.not_in(subq))
        .order_by(func.random())
    )

    result = await session.execute(stmt)
    users = result.scalars().all()

    total = math.ceil(len(users) * (percent / 100))
    selected_users = users[:total]

    now = datetime.utcnow()

    new_links = [
        UserSegment(user_id=u.id, segment_id=segment_id, added_at=now)
        for u in selected_users
    ]

    session.add_all(new_links)
    await session.commit()

    return [u.id for u in selected_users]
