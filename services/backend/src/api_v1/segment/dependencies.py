from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_segment
from core.models import db_helper, Segment
from .schemas import SegmentSchema


async def get_segment_by_id(
    segment_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Segment:
    segment = await get_segment(session=session, segment_id=segment_id)
    if not segment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found")
    return segment
