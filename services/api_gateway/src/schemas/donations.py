from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class CreateApplicationRequest(BaseModel):
    user_id: int = Field(..., description="ID користувача")
    blood_type: str = Field(..., description="Група крові")
    application_time: datetime = Field(..., description="Час подання заявки")
    application_day: Optional[datetime] = Field(None, description="День подання заявки")
    location_id: Optional[str] = Field(None, description="ID локації")
    status: Optional[str] = Field("pending", description="Статус заявки")


class ApplicationResponse(BaseModel):
    application_id: int
    user_id: int
    blood_type: str
    application_time: Optional[datetime]
    application_day: Optional[datetime]
    location_id: Optional[str]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class GetApplicationsResponse(BaseModel):
    applications: List[ApplicationResponse]


class CancelApplicationRequest(BaseModel):
    application_id: int = Field(..., description="ID заявки для відміни")


class CancelApplicationResponse(BaseModel):
    application_id: int
    success: bool
    message: str


class CreateApplicationResponse(BaseModel):
    application_id: int
    success: bool
    message: str
