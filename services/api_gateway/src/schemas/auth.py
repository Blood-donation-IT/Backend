from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str
    
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    token: str 

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# --- RESPONSES  ---

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"