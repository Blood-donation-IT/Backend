import datetime
from typing import Any, Dict, Optional, List

from sqlalchemy import any_, select
from src.domain.irepositories.i_user_repository import IUserRepository
from user_profile_models.user_orm import UserORM
from user_profile_models.health_test_orm import HealthTestResultORM
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
            orm_user.name = user.name
            orm_user.email = user.email
            orm_user.phone = user.phone
            orm_user.blood_type = user.blood_type
            orm_user.is_verified = user.is_verified
            orm_user.is_active = user.is_active
            orm_user.is_banned = user.is_banned
            orm_user.roles = user.roles or ["donor"]
            if user.password_hash is not None:
                orm_user.password_hash = user.password_hash
            orm_user.avatar = getattr(user, "avatar", None)
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

    async def upsert_health_test_result(
        self,
        user_id: int,
        completed_at: datetime.datetime,
        answers: Dict[int, bool],
        blood_type: Optional[str],
    ) -> None:
        await self._ensure_clean_transaction()
        try:
            row = await self._session.get(HealthTestResultORM, user_id)
            payload = {
                "completed_at": completed_at,
                "q1": answers[1],
                "q2": answers[2],
                "q3": answers[3],
                "q4": answers[4],
                "q5": answers[5],
                "q6": answers[6],
                "blood_type": blood_type,
            }
            if row:
                for k, v in payload.items():
                    setattr(row, k, v)
            else:
                self._session.add(HealthTestResultORM(user_id=user_id, **payload))
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def get_health_test_result(self, user_id: int) -> Optional[dict[str, Any]]:
        await self._ensure_clean_transaction()
        row = await self._session.get(HealthTestResultORM, user_id)
        if not row:
            return None
        return {
            "user_id": row.user_id,
            "completed_at": row.completed_at,
            "q1": row.q1,
            "q2": row.q2,
            "q3": row.q3,
            "q4": row.q4,
            "q5": row.q5,
            "q6": row.q6,
            "blood_type": row.blood_type,
            "created_at": row.created_at,
        }