from contextlib import asynccontextmanager
from src.infrastructure.db.base import get_session
from src.infrastructure.repositories.sqlalchemy_authorization_repository import SQLAlchemyAuthorizationRepository

@asynccontextmanager
async def get_authorization_repo():
    """async fabric for authorization repository"""
    async with get_session() as session:
        repo = SQLAlchemyAuthorizationRepository(session=session)
        yield repo
