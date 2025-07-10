
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class UserSegmentBaseSchema(BaseModel):
    user_id: int = Field(..., ge=1)
    segment_id: int = Field(..., ge=1)
    source: str = "manual"

class UserSegmentCreateSchema(UserSegmentBaseSchema):
    pass

class UserSegmentSchema(UserSegmentBaseSchema):
    added_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
