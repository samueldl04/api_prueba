
from datetime import datetime

from fastapi import HTTPException, logger,status

from app.models.record import Record
# data_room.id_room,type_record,record,db,current_user.id,current_user.company_id
def create_record(id_romm,type_record,record,db,user_id,company_id):
    if record is None or record.user_id is None:

        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

        new_record = record.Record(
            company_id=company_id,
            user_id=user_id,
            room_id=id_romm,
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