from contextlib import asynccontextmanager
from src.infrastructure.db.base import get_session
from services.authorization.src.infrastructure.repositories.sqlalchemy_authorization_repository import SQlAlchemyUserRepository

@asynccontextmanager
async def get_user_repo():
    """async fabric for user repository"""
    async with get_session() as session:
        repo = SQlAlchemyUserRepository(session=session)
        yield repo