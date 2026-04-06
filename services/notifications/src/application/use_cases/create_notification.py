import datetime
from typing import Optional

from src.domain.entities.notification import Notification
from src.domain.irepositories.i_notification_repository import INotificationRepository
from src.domain.services.i_id_generator import IIDGenerator


class CreateNotificationUseCase:
    def __init__(self, repository: INotificationRepository, id_generator: IIDGenerator):
        self.repository = repository
        self.id_generator = id_generator

    async def execute(
        self,
        user_id: int,
        title: str,
        message: str,
        type: int,
        created_at: Optional[datetime.datetime] = None,
    ) -> Notification:
        notification = Notification(
            id=self.id_generator.generate(),
            user_id=user_id,
            title=title or "",
            message=message,
            created_at=created_at or datetime.datetime.utcnow(),
            is_read=False,
            type=type,
        )
        await self.repository.save(notification)
        return notification
