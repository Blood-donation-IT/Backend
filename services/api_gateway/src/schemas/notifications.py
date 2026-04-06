from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class NotificationType(str, Enum):
    NOTIFICATION_TYPE_UNKNOWN = "NOTIFICATION_TYPE_UNKNOWN"
    DONATION_REMINDER = "DONATION_REMINDER"
    DONATION_UPDATE = "DONATION_UPDATE"
    ACCOUNT_UPDATE = "ACCOUNT_UPDATE"
    SYSTEM_MESSAGE = "SYSTEM_MESSAGE"


class NotificationResponse(BaseModel):
    notification_id: int
    user_id: int
    title: str
    message: str
    created_at: Optional[datetime] = None
    is_read: bool
    type: NotificationType


class GetNotificationsResponse(BaseModel):
    notifications: List[NotificationResponse]


class MarkAsReadRequest(BaseModel):
    notification_ids: List[int]


class MarkAsReadResponse(BaseModel):
    success: bool
    message: str


class CreateNotificationRequest(BaseModel):
    user_id: int
    title: str
    message: str
    type: NotificationType


class CreateNotificationResponse(BaseModel):
    notification_id: int
    success: bool
    message: str
