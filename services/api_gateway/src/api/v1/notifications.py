from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_notifications_grpc_client
from src.core.auth import get_current_user_id
from src.infrastructure.grpc.notifications_client import NotificationsGrpcClient
from src.schemas.notifications import (
    GetNotificationsResponse,
    MarkAsReadRequest,
    MarkAsReadResponse,
    CreateNotificationRequest,
    CreateNotificationResponse,
)

router = APIRouter(tags=["Notifications"])


@router.get("/notifications/get_notifications", response_model=GetNotificationsResponse)
async def get_notifications(
    user_id: Annotated[int, Depends(get_current_user_id)],
    only_unread: bool = False,
    limit: int = 50,
    offset: int = 0,
    client: NotificationsGrpcClient = Depends(get_notifications_grpc_client),
):
    try:
        result = await client.get_notifications(
            user_id=user_id,
            only_unread=only_unread,
            limit=limit,
            offset=offset,
        )
        return GetNotificationsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/notifications/mark_read", response_model=MarkAsReadResponse)
async def mark_as_read(
    body: MarkAsReadRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: NotificationsGrpcClient = Depends(get_notifications_grpc_client),
):
    try:
        result = await client.mark_as_read(user_id, body.notification_ids)
        return MarkAsReadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/notifications/create_notification", response_model=CreateNotificationResponse)
async def create_notification(
    body: CreateNotificationRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: NotificationsGrpcClient = Depends(get_notifications_grpc_client),
):
    try:
        result = await client.create_notification(
            user_id=user_id,
            title=body.title,
            message=body.message,
            type=body.type,
        )
        return CreateNotificationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
