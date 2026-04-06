from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from notifications_models.notification_orm import NotificationORM
from src.domain.entities.notification import Notification
from src.domain.irepositories.i_notification_repository import INotificationRepository


class SQLAlchemyNotificationRepository(INotificationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, orm: NotificationORM) -> Notification:
        return Notification(
            id=orm.id,
            user_id=orm.user_id,
            title=orm.title,
            message=orm.message,
            created_at=orm.created_at,
            is_read=orm.is_read,
            type=orm.type,
        )

    async def save(self, notification: Notification) -> None:
        orm = NotificationORM(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            created_at=notification.created_at,
            is_read=notification.is_read,
            type=notification.type,
        )
        self._session.add(orm)
        await self._session.commit()

    async def get_by_user_id(
        self, user_id: int, only_unread: bool = False, limit: int = 50, offset: int = 0
    ) -> List[Notification]:
        stmt = select(NotificationORM).where(NotificationORM.user_id == user_id)
        if only_unread:
            stmt = stmt.where(NotificationORM.is_read.is_(False))
        stmt = stmt.order_by(NotificationORM.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return [self._to_entity(x) for x in result.scalars().all()]

    async def mark_as_read(self, user_id: int, notification_ids: list[int]) -> int:
        if not notification_ids:
            return 0
        stmt = (
            update(NotificationORM)
            .where(
                NotificationORM.user_id == user_id,
                NotificationORM.id.in_(notification_ids),
            )
            .values(is_read=True)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount or 0

    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        orm = await self._session.get(NotificationORM, notification_id)
        return self._to_entity(orm) if orm else None
