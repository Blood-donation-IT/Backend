from datetime import date, datetime
from typing import Optional, Literal
from enum import Enum
from pydantic import BaseModel, ConfigDict

BloodType = Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "N/A"]


class UserRole(str, Enum):
    UNKNOWN = "UNKNOWN"
    DONOR = "DONOR"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"


class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    last_donation: Optional[date] = None
    total_donations: int
    blood_type: str
    lives_saved_count: int
    donor_status: str
    has_donor_book: bool
    test_is_done: bool
    birth_date: Optional[date] = None
    roles: list[UserRole] = []
    is_active: bool
    is_banned: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class EditProfileRequest(BaseModel):
    name: Optional[str] = None
    blood_type: Optional[str] = None
    avatar: Optional[str] = None
