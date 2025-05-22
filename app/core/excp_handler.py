from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

class TimporaValidationError(Exception):
    """Excepción personalizada para errores de validación en lógica"""
    pass

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Verifica si la solicitud espera una respuesta HTML
    accept_header = request.headers.get("accept", "")
    wants_html = "text/html" in accept_header
    
    if wants_html:
        # Redirige a la página correspondiente al código de error
        return RedirectResponse(url=f"/excp/{exc.status_code}")
    
    # Para API o solicitudes que no esperan HTML, devuelve JSON
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )