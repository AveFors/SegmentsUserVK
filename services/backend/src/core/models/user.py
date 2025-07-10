from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

class User(Base):
    __tablename__ = "users"

    external_id: Mapped[int] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    segments: Mapped[list["UserSegment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
