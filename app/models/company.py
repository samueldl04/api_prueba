from datetime import date
from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.record import Record
    from app.models.employee import Employee
    from app.models.rooms import Rooms


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    cif: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    

    # Relación con la asociación usuario-compañía-rol
    devices: Mapped[List["Device"]] = relationship("Device", back_populates="company")
    records: Mapped[List["Record"]] = relationship("Record", back_populates="company")
    employee: Mapped[List["Employee"]] = relationship("Employee", back_populates="company")
    rooms: Mapped[List["Rooms"]] = relationship("Rooms", back_populates="company")