from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255, description="Password must be at least 8 characters")
    confirm_password: str = Field(..., min_length=8, max_length=255, description="Password confirmation must match password")
    
    @model_validator(mode='after')
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and confirm_password do not match")
        return self

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    token: str 

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# --- RESPONSES  ---

class RegisterResponse(BaseModel):
    user_id: int
    email: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: Optional[int] = None
    email: Optional[str] = None