from fastapi import HTTPException, Request
from app.core.security import decode_access_token
from app.models.employee import Employee
from typing import Optional
from app.db import session


def get_user_by_dni(db: session, dni: str, password: Optional[int] = None):
    # dni_deterministic_hash = get_deterministic_hash(dni)
    user = db.query(Employee).filter(Employee.dni == dni).first()
    print(f"user{user} Tipo{type(user)}")
    if not user:
        return {
            "error": "user_not_found",
            "message": f"No se encontró ningún usuario con DNI {dni}."
        }
    print(f"Contraseña{password} almacenada{user.password} ")
    if password:
        if user.password != password:
            return {
                "error": "incorrect_password",
                "message": "La contraseña introducida es incorrecta"
            }
    else:
        pass
    
    user.company_id = user.company.id
    return {"user": user}

def authenticate_user(db: session, dni: str, password: str):

    
    result_get_user = get_user_by_dni(db, dni, password)
    if "error" in result_get_user:
        return result_get_user

    return result_get_user

def get_user_from_access_token(request: Request, db: session) -> Employee:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=402, detail="No autenticado")
    
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    dni = payload.get("dni")
    company_id = payload.get("company_id")
    if not dni:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    user_result = get_user_by_dni(db, dni, company_id)
    if "error" in user_result:
        raise HTTPException(status_code=404, detail=user_result["message"])
    
    return user_result["user"]