import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base,DeclarativeMeta

# from src.config import DATABASE_URL

# from services.user_profile.src.infrastructure.db.models.user_orm import *

logging.basicConfig(level=logging.DEBUG) 

Base:DeclarativeMeta = declarative_base()
