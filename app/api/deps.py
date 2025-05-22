from fastapi import Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session



from app.db.session import get_db

from app.services.auth_service import get_user_by_dni, decode_access_token

templates = Jinja2Templates(directory="app/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)
db = next(get_db())


# def template_has_permission(user_id, company_id, permission_code):
#     """Función auxiliar para verificar permisos en templates"""
#     with db:

#         # Obtengamos todos los permisos y verifiquemos si el código está entre ellos
#         result = rbac_service.has_permission(user_id, company_id, permission_code)
#         return result
# templates.env.globals["has_permission"] = template_has_permission
# templates.env.globals.update(asset_path=asset_path)

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Obtener token desde cabecera o cookie
    if not token:
        print(f"No hay token")
        token = request.cookies.get("access_token")
        print(token)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se proporcionó token de acceso",
                headers={"WWW-Authenticate": "Bearer"},
            )
    try:
        print("Entra")
        payload = decode_access_token(token)
        dni = payload.get("dni")
        # company_id = payload.get("company_id")
        print(dni)
        if dni is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no válido",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Se pasa el company_id obtenido desde el token para validar la asociación
    user_result = get_user_by_dni(db, dni)
    print(user_result)
    if not user_result or "error" in user_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_result["user"]

