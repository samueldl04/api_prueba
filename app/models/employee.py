from datetime import date, datetime
import hashlib
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Date, ForeignKey, Index, String, Integer, Time, Boolean, DateTime, Enum as SAEnum, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base



if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.record import Record
    from app.models.role_employee import RoleEmployee
    

class Employee(Base):
    __tablename__ = "employee"
    

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dni: Mapped[str] = mapped_column(String(9), nullable=False)
    
    email: Mapped[str] =mapped_column(String(128), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(15), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role_employee.id"), nullable=False)

    type_role: Mapped["RoleEmployee"] = relationship("RoleEmployee", back_populates="role")
    records: Mapped["Record"] = relationship("Record", back_populates="employer")
    company: Mapped["Company"] = relationship("Company", back_populates="employee")


