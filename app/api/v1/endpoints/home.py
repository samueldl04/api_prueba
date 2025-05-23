import asyncio
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, Response, logger, status, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from app import db
from app.models.employee import Employee
from app.models.record import Record
from app.models.record_type import RecordType
from app.models.rooms import Rooms
from app.schemas.notificacion import Data_room, Espesific_room
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
from app.services.home_service import create_record
from app.services.notificaiones_service import trigger_relay_sync


router = APIRouter()

@router.get("/data", summary="Obtener la informacion para mostrar en el home", tags=["Home"])
async def get_home_data(
    floor: int | None = Query(None),
    room: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Rooms).filter(
        Rooms.company_id == current_user.company_id
    )
    if floor is not None:
        query = query.filter(Rooms.floor == floor)
    if room is not None:
        query = query.filter(Rooms.room_number == room)
    
    rooms = query.all()
    print("Entra en la ruta /data")
    print(rooms)  
    rooms_data = [
        {
            "id": room.id,
            "call_point": room.call_point,
            "room": room.room_number,
            "floor": room.floor,
            "detail_call_point": room.detail_call_point,
        }
        for room in rooms
    ]
    
    return JSONResponse(content=rooms_data)
    


@router.get("/status/{espesific_room}", summary="Obtener la informacion para mostrar en el home", tags=["Home"])
async def get_home_data(
    espesific_room: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    rooms = db.query(
        Record.record_type_id,
        RecordType.name.label('status_name')
    ).join(
        RecordType,
        Record.record_type_id == RecordType.id
    ).filter(
        Record.company_id == current_user.company_id
    ).filter(
        Record.room_id == espesific_room
    ).order_by(
        desc(Record.date_record),
        desc(Record.time_record)
    ).first()
    print(f"Estatusa room {rooms.record_type_id}")
    # Modificar también el rooms_data para reflejar los nuevos campos
    if rooms:
        rooms_data = {
            "status_id": rooms.record_type_id,
            "status_name": rooms.status_name
        }
    else:
        rooms_data = {
        "status_id": 1,  
        "status_name": "Sin estado"  
    }

    return JSONResponse(content=rooms_data)

@router.post("/presencia", summary="Obtener la informacion para mostrar en el home", tags=["Home"])
async def presencia(
    espesific_room: Espesific_room,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = db.query(
        Record.record_type_id,
        Record.user_id,
        Rooms.ip_room,
        RecordType.name.label('status_name'),
        Employee.first_name,
        Employee.last_name,
        Employee.company_id
        
    ).join(
        RecordType,
        Record.record_type_id == RecordType.id
    ).join(
        Employee,
        Record.user_id == Employee.id,
        isouter=True
    ).join(
        Rooms,
        Record.room_id == Rooms.id,
        isouter=True
    ).filter(
        Record.company_id == current_user.company_id
    ).filter(
        Record.room_id == espesific_room.espesific_room
    ).order_by(
        desc(Record.date_record),
        desc(Record.time_record)
    ).first()
    if record and record.ip_room:
        url = f"http://{record.ip_room}/relay/0?turn=off"
        asyncio.create_task(trigger_relay_sync(url))

    type_record = 4
    if record.record_type_id == 3:
    

        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

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


    else:
        
   
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No hay ningun usuario que haya aceptado la llamada"
        )






@router.post("/accept_call", summary="Obtener la informacion para mostrar en el home", tags=["Home"])
async def get_home_data(
    data_room: Data_room,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    record = db.query(
        Record.record_type_id,
        Record.user_id,
        RecordType.name.label('status_name'),
        Employee.first_name,
        Employee.last_name,
        Employee.company_id
    ).join(
        RecordType,
        Record.record_type_id == RecordType.id
    ).join(
        Employee,
        Record.user_id == Employee.id,
        isouter=True
    ).filter(
        Record.company_id == current_user.company_id
    ).filter(
        Record.room_id == data_room.id_room
    ).order_by(
        desc(Record.date_record),
        desc(Record.time_record)
    ).first()
    type_record = 3
    print(record)

    # create_record(data_room.id_room,type_record,record,db,current_user.id,current_user.company_id)

    if record is None or record.user_id is None:

        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

        new_record = Record(
            company_id=current_user.company_id,
            user_id=current_user.id,
            room_id=data_room.id_room,
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


    else:
        
        if record.first_name and record.last_name:
            employee_name = f"{record.first_name} {record.last_name}"
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya se acepto la llamada por el empleado {employee_name}"
        )

