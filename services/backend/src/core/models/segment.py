from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from core.models.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.user_segment import UserSegment

class Segment(Base):
    __tablename__ = "segments"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[List["UserSegment"]] = relationship(back_populates="segment", cascade="all, delete-orphan")
