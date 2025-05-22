from fastapi import APIRouter
from app.api.v1.endpoints import auth, admin, notificaciones, home


api_router_v1 = APIRouter()

# Endpoint para autenticación (login, registro, etc.)
api_router_v1.include_router(auth.router, prefix="/auth", tags=["Autenticación"])

api_router_v1.include_router(admin.router, prefix="/admin", tags=["Administracion"])

api_router_v1.include_router(notificaciones.router, prefix="/notificacion", tags=["notificaciones"])

api_router_v1.include_router(home.router, prefix="/home", tags=["principal"])

