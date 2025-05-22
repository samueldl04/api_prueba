from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from app.models.employee import Employee
from app.models.role_employee import RoleEmployee
from app.models.company import Company 
from app.models.rooms import Rooms
from app.models.record import Record
from app.models.record_type import RecordType
from app.services.auth_service import authenticate_user

from app.core.security import create_access_token
from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import (
    PassChange as PassChangeSchema, 
    Login as LoginSchema,
    ForgotPassword as ForgotPasswordSchema,
    ResetPassword as ResetPasswordSchema,
    PolicySignatureRequest as PolicySignature
)
from app.api.deps import get_current_user, templates

router = APIRouter()

@router.post("/employee", summary="Obtener access token y establecer cookie", tags=["Autenticación"])
async def employee(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        employee = db.query(Employee).options(
            joinedload(Employee.company_id).joinedload(Company.id),
            joinedload(Employee.role_id).joinedload(RoleEmployee.id)
        ).filter(Employee.company_id == current_user.company_id).all()
        return employee
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuarios: {str(e)}"
        )
    
@router.post("/rooms", summary="Obtener access token y establecer cookie", tags=["Autenticación"])
async def employee(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        rooms = db.query(Rooms).filter(Rooms.company_id == current_user.company_id).all()

        print(rooms)
        return rooms
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuarios: {str(e)}"
        )
@router.post("/record", summary="Obtener access token y establecer cookie", tags=["Autenticación"])
async def employee(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        employee = db.query(Record).options(
            joinedload(Record.record_type_id).joinedload(RecordType.id),
            joinedload(Record.company_id).joinedload(Company.id)
        ).filter(Employee.company_id == current_user.company_id).all()
        return employee
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuarios: {str(e)}"
        )

@router.post("/create_user", summary="Obtener access token y establecer cookie", tags=["Autenticación"])
async def employee(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        new_record = Record(
            company_id=current_user.company_id,
            user_id=current_user.id,
            room_id=espesific_room.espesific_room,
            record_type_id=type_record,
            details="",  # Usar fecha del cliente
            date_record=current_date,  # Usar hora del cliente
            time_record=current_time,
            
        )
        try:
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
        except Exception as e:
            db.rollback()
            logger.error(f"Error interno al registrar la asignacion de la llamada: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno al registrar la asignacion de la llamada."
            )
        return new_record
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuarios: {str(e)}"
        )