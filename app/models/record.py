from datetime import date, datetime, time
from typing import TYPE_CHECKING
from sqlalchemy import Date, Integer, Boolean, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


if TYPE_CHECKING:
    from app.models.rooms import Rooms  # Actualizado
    from app.models.company import Company
    from app.models.employee import Employee
    from app.models.record_type import RecordType

def current_date():
    return date.today()

def current_time():
    return datetime.now().time()


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("employee.id"), nullable=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    record_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("record_type.id"), nullable=False)
    details: Mapped[str] = mapped_column(String(100), nullable=True)
    
    date_record: Mapped[date] = mapped_column(Date, nullable=False, default=current_date)
    time_record: Mapped[time] = mapped_column(Time, nullable=False, default=current_time)

    # Relaciones
    company: Mapped["Company"] = relationship("Company", back_populates="records")
    employer: Mapped["Employee"] = relationship("Employee", back_populates="records")
    rooms: Mapped["Rooms"] = relationship("Rooms", back_populates="records")
    record_type: Mapped["RecordType"] = relationship("RecordType", back_populates="records")