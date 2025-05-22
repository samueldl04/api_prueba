from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

status_code_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@status_code_router.get("/401", response_class=HTMLResponse)
async def unauthorized(request: Request):
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@status_code_router.get("/403", response_class=HTMLResponse)
async def forbidden(request: Request):
    return templates.TemplateResponse("status_code/403.html", {"request": request}, status_code=403)

@status_code_router.get("/404", response_class=HTMLResponse)
async def not_found(request: Request):
    return templates.TemplateResponse("status_code/404.html", {"request": request}, status_code=404)

@status_code_router.get("/500", response_class=HTMLResponse)
async def server_error(request: Request):
    return templates.TemplateResponse("status_code/500.html", {"request": request}, status_code=500)

