import datetime

from sqlalchemy import select
from src.domain.irepositories.i_application_repository import IApplicationRepository
from typing import Optional, List
from src.infrastructure.db.models.application_orm import ApplicationORM
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.application import Application
from sqlalchemy.exc import NoResultFound

class SQLAlchemyApplicationRepository(IApplicationRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_by_id(self, application_id: int) -> Optional[Application]:
        orm_app: ApplicationORM = await self._session.get(ApplicationORM, application_id)
        return orm_app.to_entity() if orm_app else None

    async def get_by_id(self, user_id: int) -> List[Application]:
        result = await self._session.execute(
            select(ApplicationORM).where(ApplicationORM.user_id == user_id)
        )
        orm_apps = result.scalars().all()
        return [app.to_entity() for app in orm_apps]

    async def save(self, application: Application) -> None:
        orm_app: ApplicationORM = ApplicationORM.from_entity(application)
        self._session.add(orm_app)
        await self._session.commit()
        return None

    async def update(self, application: Application) -> None:
        orm_app: ApplicationORM = await self._session.get(ApplicationORM, application.id)
        if not orm_app:
            raise NoResultFound(f"Application {application.id} not found")
        orm_app.user_id = application.user_id
        orm_app.blood_type = application.blood_type
        orm_app.application_time = application.application_time
        orm_app.status = application.status
        orm_app.description = application.description
        await self._session.commit()
        return None

    async def delete(self, application_id: int) -> None:
        orm_app: ApplicationORM = await self._session.get(ApplicationORM, application_id)
        if orm_app:
            await self._session.delete(orm_app)
            await self._session.commit()
        return None