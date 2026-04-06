from src.domain.irepositories.i_notification_repository import INotificationRepository


class MarkAsReadUseCase:
    def __init__(self, repository: INotificationRepository):
        self.repository = repository

    async def execute(self, notification_ids: list[int]) -> int:
        return await self.repository.mark_as_read(notification_ids)
