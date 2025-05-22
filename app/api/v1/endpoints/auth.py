from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from app.services.auth_service import authenticate_user

from app.core.security import create_access_token
from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import (
    PassChange as PassChangeSchema, 
    Login as LoginSchema,
    ForgotPassword as ForgotPasswordSchema,
    ResetPassword as ResetPasswordSchema,
    PolicySignatureRequest as PolicySignature
)
from app.api.deps import get_current_user, templates


router = APIRouter()

@router.post("/login", summary="Obtener access token y establecer cookie", tags=["Autenticación"])
async def login(
    response: Response,
    login_data: LoginSchema = Body(...),
    db: Session = Depends(get_db)
):
    auth_result = authenticate_user(db, login_data.dni, login_data.password)
    
    if "error" in auth_result:
        error = auth_result["error"]
        message = auth_result["message"]
        detail = {"error": error, "message": message}
        print("Error = ",error)
        if error == "user_not_found":
            print("no se encontro ")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            )
        elif error == "incorrect_password":
            print("La contraseña no es correcta")
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail,
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    user = auth_result["user"]
    
    
    
    # Extraer datos básicos del usuario
    user_id    = user.id 
    last_name  = user.last_name
    first_name = user.first_name
    dni        = user.dni
    email      = user.email
    company_id = user.company_id
    role_id    = user.role_id
    # Ahora work_time y break_time se obtienen de la relación usuario-empresa
    

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": user_id,
            "sub": f"{last_name}, {first_name}",
            "dni": dni,
            "company_id": company_id,
            "email": email,
            "role_id": role_id   
        },
        expires_delta=access_token_expires
    )
    print({
            "id": user_id,
            "sub": f"{last_name}, {first_name}",
            "dni": dni,
            "company_id": company_id,
            "email": email,
            "role_id": role_id
    })
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False, # Cambiar a True en producción
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Ajustar en producción
    )
    
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/logout")
async def logout(request: Response):
    response = JSONResponse(status_code=200, content={"message": "Sesión cerrada."})
    response.delete_cookie("access_token")
    return response