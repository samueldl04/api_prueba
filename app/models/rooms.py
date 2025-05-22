from datetime import date, datetime, time
from typing import TYPE_CHECKING
from sqlalchemy import Date, Integer, Boolean, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.record import Record


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    room_number: Mapped[int] = mapped_column(Integer, nullable=False)
    call_point: Mapped[str] = mapped_column(String(10), nullable=False)
    detail_call_point : Mapped[str] = mapped_column(String(100), nullable=False)    
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    # Relaciones
    company: Mapped["Company"] = relationship("Company", back_populates="rooms")
    records: Mapped["Record"] = relationship("Record", back_populates="rooms")
    
    