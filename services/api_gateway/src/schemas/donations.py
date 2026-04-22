from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


def _serialize_application_id(v: int) -> str:
    return str(v)


class CreateApplicationRequest(BaseModel):
    blood_type: str = Field(..., description="Група крові")
    application_day: datetime = Field(..., description="День запису на донацію")
    application_time: Optional[datetime] = Field(None, description="Час запису на донацію")
    slot_index: int = Field(..., ge=0, le=9, description="Слот часу")
    location_id: Optional[str] = Field(None, description="ID локації")
    status: Optional[str] = Field("pending", description="Статус заявки")


class SlotInfo(BaseModel):
    slot_index: int
    time_label: str
    booked_count: int
    capacity: int
    is_available: bool


class GetAvailableSlotsResponse(BaseModel):
    slots: List[SlotInfo]
    daily_booked: int
    daily_capacity: int
    day_available: bool = True   # false вихідні, 2 місяці+
    reason: str = ""             # "weekend" | "past" | "out_of_range"


class ApplicationResponse(BaseModel):
    application_id: int
    user_id: int
    blood_type: str
    application_time: Optional[datetime]
    application_day: Optional[datetime]
    slot_index: Optional[int] = None
    location_id: Optional[str]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @field_serializer("application_id")
    def _ser_app_id(self, v: int) -> str:
        return _serialize_application_id(v)

    @field_serializer("application_time")
    def _ser_application_time(self, v: Optional[datetime]) -> Optional[str]:
        if v is None:
            return None
        return v.strftime("H%:%M")

    @field_serializer("application_day")
    def _ser_application_day(self, v: Optional[datetime]) -> Optional[str]:
        if v is None:
            return None
        return v.strftime("%Y-%m-%d")


class GetApplicationsResponse(BaseModel):
    applications: List[ApplicationResponse]


class CancelApplicationRequest(BaseModel):
    application_id: int = Field(..., description="ID заявки для відміни")


class CancelApplicationResponse(BaseModel):
    application_id: int
    success: bool
    message: str

    @field_serializer("application_id")
    def _ser_app_id(self, v: int) -> str:
        return _serialize_application_id(v)


class GetCalendarAvailabilityResponse(BaseModel):
    available_dates: List[str]  

class CreateApplicationResponse(BaseModel):
    application_id: int
    success: bool
    message: str

    @field_serializer("application_id")
    def _ser_app_id(self, v: int) -> str:
        return _serialize_application_id(v)
