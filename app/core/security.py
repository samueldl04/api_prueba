from datetime import datetime, timedelta

import jwt

from app.core.config import settings
import base64





def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise Exception("Token inválido")
    
def valid_base64(data:str) -> bool: #Se le pasa el Base64 pero tienes que quitarle el ecabezado
    try:
        base64.b64decode(data, validate=True)
        return True
    except Exception:
        return False
    
