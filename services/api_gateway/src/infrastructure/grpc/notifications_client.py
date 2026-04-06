import grpc
from typing import Optional

from contracts.notifications import notifications_pb2, notifications_pb2_grpc
from src.schemas.notifications import NotificationType


TYPE_TO_PROTO = {
    NotificationType.NOTIFICATION_TYPE_UNKNOWN: notifications_pb2.NOTIFICATION_TYPE_UNKNOWN,
    NotificationType.DONATION_REMINDER: notifications_pb2.DONATION_REMINDER,
    NotificationType.DONATION_UPDATE: notifications_pb2.DONATION_UPDATE,
    NotificationType.ACCOUNT_UPDATE: notifications_pb2.ACCOUNT_UPDATE,
    NotificationType.SYSTEM_MESSAGE: notifications_pb2.SYSTEM_MESSAGE,
}


class NotificationsGrpcClient:
    def __init__(self, host: str, port: int):
        self.target = f"{host}:{port}"

    async def get_notifications(
        self, user_id: int, only_unread: bool = False, limit: int = 50, offset: int = 0
    ) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = notifications_pb2_grpc.NotificationsServiceStub(channel)
            request = notifications_pb2.GetNotificationsRequest(
                user_id=user_id,
                only_unread=only_unread,
                limit=limit,
                offset=offset,
            )
            response = await stub.GetNotifications(request)
            notifications = []
            for n in response.notifications:
                created_at = n.created_at.ToDatetime() if n.HasField("created_at") else None
                type_name = notifications_pb2.NotificationType.Name(n.type)
                notifications.append(
                    {
                        "notification_id": n.notification_id,
                        "user_id": n.user_id,
                        "title": n.title,
                        "message": n.message,
                        "created_at": created_at,
                        "is_read": n.is_read,
                        "type": type_name,
                    }
                )
            return {"notifications": notifications}

    async def mark_as_read(self, user_id: int, notification_ids: list[int]) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = notifications_pb2_grpc.NotificationsServiceStub(channel)
            request = notifications_pb2.MarkAsReadRequest(
                notification_ids=notification_ids, user_id=user_id
            )
            response = await stub.MarkAsRead(request)
            return {"success": response.success, "message": response.message}

    async def create_notification(
        self, user_id: int, title: str, message: str, type: NotificationType
    ) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = notifications_pb2_grpc.NotificationsServiceStub(channel)
            request = notifications_pb2.CreateNotificationRequest(
                user_id=user_id,
                title=title,
                message=message,
                type=TYPE_TO_PROTO[type],
            )
            response = await stub.CreateNotification(request)
            return {
                "notification_id": response.notification_id,
                "success": response.success,
                "message": response.message,
            }
