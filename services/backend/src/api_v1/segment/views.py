from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Segment
from api_v1.segment.schemas import (
    SegmentCreateSchema,
    SegmentSchema,
    SegmentUpdateSchema,
)
from api_v1.segment import crud
from .dependencies import get_segment_by_id

router = APIRouter(tags=["Segments"])


@router.get("/", response_model=list[SegmentSchema])
async def get_segments(session: AsyncSession = Depends(db_helper.session_getter)):
    segments = await crud.get_all_segments(session)
    return segments


@router.get("/{segment_id}", response_model=SegmentSchema)
async def get_segment(
    segment: Segment = Depends(get_segment_by_id),
):
    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found"
        )
    return segment


@router.post("/", response_model=SegmentSchema, status_code=status.HTTP_201_CREATED)
async def create_new_segment(
    segment_in: SegmentCreateSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    segment = await crud.create_segment(session, segment_in)
    return segment


@router.patch("/{segment_id}", response_model=SegmentSchema)
async def update_existing_segment(
    segment_in: SegmentUpdateSchema,
    segment: Segment = Depends(get_segment_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found"
        )
    updated_segment = await crud.update_segment(segment, segment_in, session)
    return updated_segment


@router.delete("/{segment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_segment(
    segment_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    await crud.delete_segment(segment_id, session)
    return None


@router.get("/users/{user_id}/segments", response_model=list[SegmentSchema])
async def get_segments_by_user(
    user_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    segments = await crud.get_segments_by_user(session, user_id)
    return segments
