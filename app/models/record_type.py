from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.record import Record

class RecordType(Base):
    __tablename__ = "record_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Campo adicional opcional

    # Relación con ClockIn
    records: Mapped[List["Record"]] = relationship("Record", back_populates="record_type")