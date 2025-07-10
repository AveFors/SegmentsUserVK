from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.user_segment import UserSegment

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    segments: Mapped[list["UserSegment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
