from src.domain.irepositories.i_notification_repository import INotificationRepository


class GetNotificationsUseCase:
    def __init__(self, repository: INotificationRepository):
        self.repository = repository

    async def execute(
        self, user_id: int, only_unread: bool = False, limit: int = 50, offset: int = 0
    ):
        return await self.repository.get_by_user_id(
            user_id=user_id, only_unread=only_unread, limit=limit, offset=offset
        )
