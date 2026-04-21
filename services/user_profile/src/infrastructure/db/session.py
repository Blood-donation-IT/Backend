import os
import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.DEBUG)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_async_engine(DATABASE_URL, future=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def on_startup() -> None:
    try:
        async with engine.begin() as connection:
            from user_profile_models.base import Base  
            import user_profile_models.user_orm 
            import user_profile_models.health_test_orm 
            await connection.run_sync(Base.metadata.create_all)
        logging.info("Successful DB connection")
    except Exception as e:
        logging.error(f"Error with DB connecting: {e}")


async def on_shutdown() -> None:
    await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()