from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func, String
from core.models.base import Base

if TYPE_CHECKING:
    from core.models.user import User
    from core.models.segment import Segment

class UserSegment(Base):
    __tablename__ = "user_segments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    segment_id: Mapped[int] = mapped_column(ForeignKey("segments.id", ondelete="CASCADE"), nullable=False)
    added_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    source: Mapped[str] = mapped_column(String(50), default="manual")

    user: Mapped["User"] = relationship(back_populates="segments")
    segment: Mapped["Segment"] = relationship(back_populates="users")
