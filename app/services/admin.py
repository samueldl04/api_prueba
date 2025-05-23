from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, Response, logger, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

# from app import db
from app.models.employee import Employee
 
from app.models.rooms import Rooms
from app.models.record import Record
from app.models.record_type import RecordType


from app.api.deps import get_current_user, templates


async def obtein_data(type_consulta,db,current_user):
    if type_consulta == "camas":
        query = db.query(Rooms).filter(
            Rooms.company_id == current_user.company_id
        ).all()

        rooms_data = [
            {
                "id": room.id,
                "call_point": room.call_point,
                "room": room.room_number,
                "floor": room.floor,
                "detail_call_point": room.detail_call_point,
            }
            for room in query
        ]
        
        return JSONResponse(content=rooms_data)
    
    elif type_consulta == "registros":
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
        
        return JSONResponse(content=registro_data)  # Corregido el nombre de la variable
        
    elif type_consulta == "empleados":
        query = db.query(Employee).filter(
            Employee.company_id == current_user.company_id
        ).filter(
            Employee.active == True
        ).all()
        empleados_data = [
            {
                "id": room.id,
                "dni": room.dni,
                "email": room.email,
                "phone_number": room.phone_number,
                "first_name": room.first_name,
                "last_name": room.last_name,
                "password": room.password,
                "status": room.status,        
            }
            for room in query
        ]
        
        return JSONResponse(content=empleados_data)