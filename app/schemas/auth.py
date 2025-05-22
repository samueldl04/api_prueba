from typing import Optional
from pydantic import BaseModel, field_validator

class Login(BaseModel):
    dni: str
    password: str
    

class PassChange(BaseModel):
    old_password: str
    new_password: str

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    token: str
    new_password: str

class PolicySignatureRequest(BaseModel):
    dni: str
    password: str
    company_id: int
    signature: str  # base64 string
    accepted: bool