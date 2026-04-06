import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from contracts.notifications import notifications_pb2, notifications_pb2_grpc
from src.application.use_cases.get_notifications import GetNotificationsUseCase
from src.application.use_cases.mark_as_read import MarkAsReadUseCase
from src.application.use_cases.create_notification import CreateNotificationUseCase
from src.domain.entities.notification import Notification


def _to_proto(notification: Notification) -> "notifications_pb2.Notification":
    ts = Timestamp()
    if notification.created_at:
        ts.FromDatetime(notification.created_at)
    return notifications_pb2.Notification(
        notification_id=notification.id,
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        created_at=ts if notification.created_at else None,
        is_read=notification.is_read,
        type=notification.type,
    )


class NotificationsService(notifications_pb2_grpc.NotificationsServiceServicer):
    def __init__(
        self,
        get_notifications_use_case: GetNotificationsUseCase,
        mark_as_read_use_case: MarkAsReadUseCase,
        create_notification_use_case: CreateNotificationUseCase,
    ):
        self.get_notifications_use_case = get_notifications_use_case
        self.mark_as_read_use_case = mark_as_read_use_case
        self.create_notification_use_case = create_notification_use_case

    async def GetNotifications(self, request, context):
        try:
            notifications = await self.get_notifications_use_case.execute(
                user_id=request.user_id,
                only_unread=request.only_unread,
                limit=request.limit if request.limit > 0 else 50,
                offset=request.offset if request.offset >= 0 else 0,
            )
            return notifications_pb2.GetNotificationsResponse(
                notifications=[_to_proto(n) for n in notifications]
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return notifications_pb2.GetNotificationsResponse()

    async def MarkAsRead(self, request, context):
        try:
            updated = await self.mark_as_read_use_case.execute(
                list(request.notification_ids)
            )
            return notifications_pb2.MarkAsReadResponse(
                success=True, message=f"Marked as read: {updated}"
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return notifications_pb2.MarkAsReadResponse(success=False, message=str(e))

    async def CreateNotification(self, request, context):
        try:
            notification = await self.create_notification_use_case.execute(
                user_id=request.user_id,
                title=request.title,
                message=request.message,
                type=request.type,
            )
            return notifications_pb2.CreateNotificationResponse(
                notification_id=notification.id,
                success=True,
                message="Notification created",
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return notifications_pb2.CreateNotificationResponse(
                notification_id=0, success=False, message=str(e)
            )
