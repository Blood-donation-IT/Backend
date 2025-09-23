import datetime

from sqlalchemy import any_, select
from src.domain.irepositories.i_user_repository import IUserRepository
from typing import Optional, List
from src.infrastructure.db.models.user_orm import UserORM
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from sqlalchemy.exc import NoResultFound

class SQlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
    async def get_user_by_id(self, user_id:int) -> Optional[User]:
        orm_user: UserORM = await self._session.get(UserORM, user_id)
        return orm_user.to_entity() if orm_user else None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        orm_user: UserORM = await self._session.execute(
            UserORM.select().where(UserORM.email == email)
        )
        orm_user = orm_user.scalar_one_or_none()
        return orm_user.to_entity() if orm_user else None
    
    async def save(self, user: User) -> None:
        orm_user: UserORM = UserORM.from_entity(user)
        self._session.add(orm_user)
        await self._session.commit()
        return None
    
    async def delete(self, user_id: int) -> None:
        orm_user: UserORM = await self._session.get(UserORM, user_id)
        if orm_user:
            await self._session.delete(orm_user)
            await self._session.commit()
        return None
    async def list_active_donors(self, limit: int = 100) -> List[User]:
        result = await self._session.execute(
            select(UserORM).where(UserORM.is_active == True, "donor" == any_(UserORM.roles)).limit(limit)
        )
        orm_users = result.scalars().all()
        return [u.to_entity() for u in orm_users]
    
    async def get_last_donation_date(self, user_id: int) -> Optional[datetime.datetime]:
        orm_user = await self._session.get(UserORM, user_id)
        return orm_user.last_donation_at if orm_user and orm_user.last_donation_at else None