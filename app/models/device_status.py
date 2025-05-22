from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.device import Device

class DeviceStatus(Base):
    __tablename__ = "device_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Campo adicional opcional

    # Relación con ClockIn
    devices: Mapped[List["Device"]] = relationship("Device", back_populates="device_status")