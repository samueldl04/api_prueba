from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.routers import api_router_v1
from app.core.excp_handler import custom_http_exception_handler
from app.core.excp_router import status_code_router
from app.core.loggin import configure_logging
from app.db.base import Base
from app.db.session import engine, get_db
from app.api.deps import get_current_user, templates
from sqlalchemy.orm import Session

# Crea todas las tablas definidas en los modelos (si no existen)
Base.metadata.create_all(bind=engine)

# Logging
configure_logging()

# Fastapi instance
app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0",)

# Exception handler
app.add_exception_handler(HTTPException, custom_http_exception_handler)

# Middlewares
@app.middleware("http")
async def add_auth_service_to_request(request: Request, call_next):
    """Añade el servicio de autorización a la solicitud para uso en plantillas"""
    db = next(get_db())
    response = await call_next(request)
    return response

# Montar directorios estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rotes
app.include_router(api_router_v1, prefix="/api/v1")
app.include_router(status_code_router, prefix="/excp")

@app.get("/", response_class=HTMLResponse, summary="Fichajes")
async def login(request: Request, db: Session = Depends(get_db)):
    #from app.utils.rbac.migrate_to_rbac import migrate_data
    #migrate_data(db)
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse, summary="Fichajes - Login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@app.get("/home", response_class=HTMLResponse, summary="Fichajes - Inicio")
async def home(request: Request, current_user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "current_user": current_user,
        "active_page": "home",
        "page_icon": "dashboard",
        "page_title": "Panel de control"
    })

@app.get("/admin", response_class=HTMLResponse, summary="Fichajes - Inicio")
async def admin(request: Request, current_user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "current_user": current_user,
        "active_page": "admin",
        "page_icon": "dashboard",
        "page_title": "Panel de control"
    })

@app.get("/detail", response_class=HTMLResponse, summary="Fichajes - Inicio")
async def home(request: Request, current_user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("detail_call.html", {
        "request": request,
        "current_user": current_user,
        "active_page": "detail_call",
        "page_icon": "dashboard",
        "page_title": "Panel de control"
    })




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main", host=settings.HOST, port=settings.PORT, reload=True)