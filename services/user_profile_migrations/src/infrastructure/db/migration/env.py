from logging.config import fileConfig
import sys, os

# Получаем абсолютный путь до корня проекта (где лежит libs/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../.."))
LIBS_PATH = os.path.join(BASE_DIR, "libs/user_profile/src")

sys.path.append(LIBS_PATH)
from sqlalchemy import create_engine, pool
from alembic import context

from user_profile_models.base import Base  # noqa
from user_profile_models.user_orm import UserORM  # noqa: F401

target_metadata = Base.metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    database_url = os.getenv("DATABASE_URL","postgresql+psycopg2://user:password@localhost:5433/user_profile_db")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set in environment!")
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    database_url = os.getenv("DATABASE_URL","postgresql+psycopg2://user:password@localhost:5433/user_profile_db")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set in environment!")

    connectable = create_engine(database_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()