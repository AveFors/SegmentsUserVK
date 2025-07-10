from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SegmentBaseSchema(BaseModel):
    name: str
    description: str | None = None


class SegmentCreateSchema(SegmentBaseSchema):
    pass

class SegmentUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None

class SegmentSchema(SegmentBaseSchema):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
