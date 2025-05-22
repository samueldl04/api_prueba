from app.db.base import Base
from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.device_status import DeviceStatus
    from app.models.company import Company

class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip_device: Mapped[str] = mapped_column(String(20), nullable=False)
    device_status_id: Mapped[int] = mapped_column(Integer, ForeignKey("device_status.id"), nullable=False)
    id_company: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)

    # Relación con DeviceStatus
    device_status: Mapped["DeviceStatus"] = relationship("DeviceStatus", back_populates="devices")
    company: Mapped["Company"] = relationship("Company", back_populates="devices")