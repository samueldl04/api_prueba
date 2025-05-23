import tempfile
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, Response, logger, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse,StreamingResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
import pandas as pd
import io
# from app import db
from app.models.employee import Employee
from app.models.role_employee import RoleEmployee
from app.models.company import Company 
from app.models.rooms import Rooms
from app.models.record import Record
from app.models.record_type import RecordType
from app.schemas.admin import Delete_user, New_User, Update_User

from app.services.admin import obtein_data
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
    
@router.get("/{type_consulta}", summary="Obtener la informacion para mostrar en el home", tags=["Home"])
async def get_admin_data(
    type_consulta: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
   return await obtein_data(type_consulta,db,current_user)
        

    
   

@router.post("/create_user", summary="Crear nuevo usuario", tags=["Autenticación"])
async def create_user(
    data_new_user: New_User,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        new_record = Employee(
            dni=data_new_user.dni,
            email=data_new_user.email,
            phone_number=data_new_user.phone_number,
            first_name=data_new_user.first_name,
            last_name=data_new_user.last_name,
            password=data_new_user.password,
            company_id=current_user.company_id,
            role_id=1,  # Default role_id
            status=True,
            active=True
        )
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Usuario creado exitosamente",
                "user": {
                    "id": new_record.id,
                    "dni": new_record.dni,
                    "email": new_record.email,
                    "first_name": new_record.first_name,
                    "last_name": new_record.last_name
                }
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/update_user", summary="Actualizar usuario existente", tags=["Autenticación"])
async def update_user(

    data_update: Update_User,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Buscar el usuario existente
        existing_user = db.query(Employee).filter(
            Employee.id == data_update.id,
            Employee.company_id == current_user.company_id
        ).first()
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Actualizar solo los campos que no son None
        if data_update.dni is not None:
            existing_user.dni = data_update.dni
        if data_update.email is not None:
            existing_user.email = data_update.email
        if data_update.phone_number is not None:
            existing_user.phone_number = data_update.phone_number
        if data_update.first_name is not None:
            existing_user.first_name = data_update.first_name
        if data_update.last_name is not None:
            existing_user.last_name = data_update.last_name
        
        db.commit()
        db.refresh(existing_user)
        
        return {
            "message": "Usuario actualizado exitosamente",
            "user": {
                "id": existing_user.id,
                "dni": existing_user.dni,
                "email": existing_user.email,
                "first_name": existing_user.first_name,
                "last_name": existing_user.last_name
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar usuario. Por favor, intente nuevamente."
        )
    
from fastapi import Body

@router.put("/delete_user", summary="Eliminar usuario existente", tags=["Autenticación"])
async def delete_user(
    id: int = Body(..., embed=True),  # ← así FastAPI toma "id" del JSON
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("ID recibido:", id)
    existing_user = (
        db.query(Employee)
          .filter(
             Employee.id == id,
             Employee.company_id == current_user.company_id
          )
          .first()
    )
    if not existing_user:
        raise HTTPException(404, "Usuario no encontrado")
    existing_user.active = False
    db.commit()
    db.refresh(existing_user)
    return {"message": "Usuario eliminado exitosamente"}

@router.get("/exportar-excel")
async def exportar_excel(
    current_user=Depends(get_current_user),
    db: Session=Depends(get_db),
):
    query = db.query(Record, RecordType).join(
            RecordType, 
            Record.record_type_id == RecordType.id
        ).filter(
            Record.company_id == current_user.company_id
        ).all()
            
    registro_data = [  # Corregido el nombre de la variable
        {
        "id": record.Record.id,
        "company_id": record.Record.company_id,
        "user_id": record.Record.user_id,
        "room_id": record.Record.room_id,
        "record_type_id": record.Record.record_type_id,
        "record_type_name": record.RecordType.name,  # Agregamos el nombre del tipo
        "details": record.Record.details,
        "date_record": record.Record.date_record.isoformat(),
        "time_record": record.Record.time_record.isoformat(),
    }
        for record in query  # Cambiado  por query
    ]
    print(registro_data)

