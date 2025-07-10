from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from api_v1.user_segment.schemas import UserSegmentCreateSchema, UserSegmentSchema
from api_v1.user_segment.crud import add_user_to_segment, remove_user_from_segment

router = APIRouter(tags=["UserSegments"])

@router.post("/", response_model=UserSegmentSchema)
async def add_to_segment(data: UserSegmentCreateSchema, session: AsyncSession = Depends(db_helper.session_getter)):
    return await add_user_to_segment(session, data)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_segment(
    user_id: int,
    segment_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await remove_user_from_segment(session, user_id, segment_id)
