from sqlalchemy import select
from src.domain.irepositories.i_authorization_repository import IAuthorizationRepository
from typing import Optional
from src.infrastructure.db.models.user_orm import AuthorizationORM
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from sqlalchemy.exc import NoResultFound

class SQLAlchemyAuthorizationRepository(IAuthorizationRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self._session.execute(
                select(AuthorizationORM).where(AuthorizationORM.email == email)
            )
            orm_user = result.scalar_one_or_none()
            return orm_user.to_entity() if orm_user else None
        except Exception as e:
            await self._session.rollback()
            raise e

    async def get_by_id(self, user_id: int) -> Optional[User]:
        orm_user: AuthorizationORM = await self._session.get(AuthorizationORM, user_id)
        return orm_user.to_entity() if orm_user else None

    async def save(self, user: User) -> None:
        try:
            orm_user: AuthorizationORM = AuthorizationORM.from_entity(user)
            self._session.add(orm_user)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        return None

    async def update(self, user: User) -> None:
        try:
            orm_user: AuthorizationORM = await self._session.get(AuthorizationORM, user.id)
            if not orm_user:
                raise NoResultFound(f"User {user.id} not found")
            orm_user.email = user.email
            orm_user.password_hash = user.password_hash
            orm_user.name = user.name
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        return None




