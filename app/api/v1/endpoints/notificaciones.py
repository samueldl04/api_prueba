import asyncio
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, logger, status
from requests import Session
from app import db
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.record import Record
from app.models.rooms import Rooms
from app.services.notificaiones_service import send_pushover_notification, trigger_relay_sync

from app.schemas.notificacion import Data_room

router = APIRouter()

TARGET_URL     = "http://localhost:8000/detail"      
URL_TITLE      = "Aceptar llamada"

@router.post("/notify")
async def notify(
    data_room: Data_room,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Construye el mensaje
        message = (
            f"¡Se ha pulsado el botón!\n"
            f"Piso: {data_room.flor}, Habitación: {data_room.room}, Cama: {data_room.bed}\n"
            "Haz clic en el enlace para obtner detalles y aceptar la llamada."
        )

        # Si quieres que el enlace incluya los parámetros:
        url = (
            f"{TARGET_URL}"
            f"?flor={data_room.flor}&room={data_room.room}&bed={data_room.bed}&id_room={data_room.id_room}"
        )

        background_tasks.add_task(
            send_pushover_notification,
            message=message,
            title="Botón Pulsado",
            priority=0,
            url=url,
            url_title=URL_TITLE
        )
        type_record = 2
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

        new_record = Record(
            company_id=current_user.company_id,
            room_id=data_room.id_room,
            record_type_id=type_record,
            details="", 
            date_record=current_date, 
            time_record=current_time,
            
        )
        try:
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            record = db.query(    
                Rooms.ip_room,
                ).filter(
                    Rooms.id == data_room.id_room
                ).first()
            
            if record and record.ip_room:
                url = f"http://{record.ip_room}/relay/0?turn=on"
                asyncio.create_task(trigger_relay_sync(url))

        except Exception as e:
            db.rollback()
            logger.error(f"Error interno al registrar la asignacion de la llamada: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno al registrar la asignacion de la llamada."
            )
        
        
        return new_record
       
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
