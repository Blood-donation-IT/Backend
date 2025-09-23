import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base,DeclarativeMeta

# from src.config import DATABASE_URL

from infrastructure.db.models import *

logging.basicConfig(level=logging.DEBUG) 

Base:DeclarativeMeta = declarative_base()
# Create an asynchronous database connection engine
# engine = create_async_engine(DATABASE_URL, future=True)
# TODO: fix env var
engine: AsyncEngine = create_async_engine(__import__("os").getenv("DATABASE_URL"), future=True)

# Create an asynchronous session for database operations
async_session:sessionmaker[AsyncSession] = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

#DOCS ONLY!
#Require psycopg2==2.9.10!
#------------------------
# import pydot
# from sqlalchemy_schemadisplay import create_schema_graph
# import graphviz

# sync_engine = create_engine(DATABASE_URL)

# graph: pydot.Dot = create_schema_graph(
#     engine=sync_engine,
#     metadata=Base.metadata,
#     show_datatypes=True, 
#     show_indexes=False,  
#     rankdir="TB", 
#     concentrate=False,  
# )
# dot_source = graph.to_string()  
# graphviz.Source(dot_source).render("schema_dsiagram", format="png")
# print("Diagram saved inschema_dsiagram.png")

#-------------------------



async def on_startup() -> None:
    """!
    Function executed at application startup.
    
    Establishes a connection to the database and creates all tables if they do not already exist.
    
    @note This is an asynchronous function using SQLAlchemy to interact with the database.
    """
    try:
        
        Base.metadata.bind = engine
        
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        logging.info("Succsesfull db connection")

    except Exception as e:
        logging.error(f"Error with db connecting: {e}")
        logging.error(f"{e}")

async def on_shutdown()->None:
    """!
    Function executed at application shutdown.
    
    Disposes the database connection.
    
    @note This is an asynchronous function that calls the `dispose` method to close the connection.
    """
    await engine.dispose()

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """!
    Provides an async context manager for a database session.

    Usage:
        async with get_session() as session:
            # use session here
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(on_startup())