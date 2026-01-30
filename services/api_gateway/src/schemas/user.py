from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict

class UserRole(str, Enum):
    UNKNOWN = "UNKNOWN"
    DONOR = "DONOR"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"

class UserProfileResponse(BaseModel):
    id: int                   
    full_name: str
    email: str
    phone: Optional[str] = None
    
    blood_type: str
    total_donations: int
    last_donation_at: Optional[datetime] = None
    avatar: Optional[str] = None
    # lives_saved_count: int = 0 

    roles: list[UserRole] = []
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class EditProfileRequest(BaseModel):
    full_name: Optional[str] = None
    blood_type: Optional[str] = None
    avatar: Optional[str] = None