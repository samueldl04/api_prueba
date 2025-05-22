from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, Response, status

from app.services.notificaiones_service import send_pushover_notification

router = APIRouter()

STATIC_MESSAGE = "¡Alerta! Se ha pulsado el botón."

@router.post("/llamada/")
async def llamar(background_tasks: BackgroundTasks):
    try:
        # Encola el envío con mensaje fijo
        background_tasks.add_task(
            send_pushover_notification,
            message=STATIC_MESSAGE,
            title="Botón Pulsado",
            priority=0
        )
        return {"status": "Envío en curso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))