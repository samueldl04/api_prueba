from typing import Optional
from pydantic import BaseModel

class New_User(BaseModel):
    dni: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role_id: int = 1

class Update_User(BaseModel):
    id: int
    dni: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password:Optional[str] = None

class Delete_user(BaseModel):
    id: int