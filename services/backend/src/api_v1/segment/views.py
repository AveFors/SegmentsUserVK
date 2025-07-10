from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Segment
from api_v1.segment.schemas import (
    SegmentCreateSchema,
    SegmentSchema,
    SegmentUpdateSchema, SegmentDistributionRequest, SegmentDistributionResponse,
)
from api_v1.segment import crud
from .crud import assign_segment_to_percent
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


@router.post("/{segment_id}/distribute", response_model=SegmentDistributionResponse)
async def distribute_segment(
    segment_id: int,
    data: SegmentDistributionRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        assigned_user_ids = await assign_segment_to_percent(
            session=session,
            segment_id=segment_id,
            percent=data.percent,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return SegmentDistributionResponse(
        assigned_user_ids=assigned_user_ids,
        count=len(assigned_user_ids),
    )