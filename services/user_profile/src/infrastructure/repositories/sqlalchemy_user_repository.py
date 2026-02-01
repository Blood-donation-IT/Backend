import datetime

from sqlalchemy import any_, select
from src.domain.irepositories.i_user_repository import IUserRepository
from typing import Optional, List
from user_profile_models.user_orm import UserORM
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from sqlalchemy.exc import NoResultFound

class SQlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def _ensure_clean_transaction(self) -> None:
        try:
            await self._session.rollback()
        except Exception:
            pass

    async def get_user_by_id(self, user_id:int) -> Optional[User]:
        await self._ensure_clean_transaction()
        orm_user: UserORM = await self._session.get(UserORM, user_id)
        return User.from_orm_dict(orm_user.to_dict()) if orm_user else None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        await self._ensure_clean_transaction()
        result = await self._session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        orm_user = result.scalar_one_or_none()
        return User.from_orm_dict(orm_user.to_dict()) if orm_user else None
    
    async def save(self, user: User) -> None:
        await self._ensure_clean_transaction()
        try:
            orm_user: UserORM = UserORM.from_entity(user)
            self._session.add(orm_user)
            await self._session.flush()
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        return None

    async def update(self, user: User) -> None:
        await self._ensure_clean_transaction()
        try:
            orm_user: UserORM = await self._session.get(UserORM, user.id)
            if not orm_user:
                raise ValueError(f"User with id {user.id} not found")
            orm_user.full_name = user.full_name
            orm_user.email = user.email
            orm_user.phone = user.phone
            orm_user.blood_type = user.blood_type
            orm_user.is_verified = user.is_verified
            orm_user.is_active = user.is_active
            orm_user.is_banned = user.is_banned
            orm_user.roles = user.roles or ["donor"]
            if user.password_hash is not None:
                orm_user.password_hash = user.password_hash
            orm_user.avatar_url = getattr(user, "avatar_url", None)
            orm_user.lives_saved_count = getattr(user, "lives_saved_count", 0) or 0
            orm_user.donor_status = getattr(user, "donor_status", None)
            orm_user.has_donor_book = getattr(user, "has_donor_book", False) or False
            orm_user.test_is_done = getattr(user, "test_is_done", False) or False
            orm_user.birth_date = getattr(user, "birth_date", None)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def delete(self, user_id: int) -> None:
        await self._ensure_clean_transaction()
        orm_user: UserORM = await self._session.get(UserORM, user_id)
        if orm_user:
            await self._session.delete(orm_user)
            await self._session.commit()
        return None
    async def list_active_donors(self, limit: int = 100) -> List[User]:
        await self._ensure_clean_transaction()
        result = await self._session.execute(
            select(UserORM).where(UserORM.is_active == True, "donor" == any_(UserORM.roles)).limit(limit)
        )
        orm_users = result.scalars().all()
        return [User.from_orm_dict(u.to_dict()) for u in orm_users]
    
    async def get_last_donation_date(self, user_id: int) -> Optional[datetime.datetime]:
        await self._ensure_clean_transaction()
        orm_user = await self._session.get(UserORM, user_id)
        return orm_user.last_donation_at if orm_user and orm_user.last_donation_at else None