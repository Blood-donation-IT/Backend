from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.notification import Notification


class INotificationRepository(ABC):
    @abstractmethod
    async def save(self, notification: Notification) -> None:
        pass

    @abstractmethod
    async def get_by_user_id(
        self, user_id: int, only_unread: bool = False, limit: int = 50, offset: int = 0
    ) -> List[Notification]:
        pass

    @abstractmethod
    async def mark_as_read(self, user_id: int, notification_ids: list[int]) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        pass
