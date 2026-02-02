"""initial authorizations table

Revision ID: 001_auth_init
Revises:
Create Date: 2025-01-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_auth_init"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Idempotent: create table only if it does not exist."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS authorizations (
            id BIGINT NOT NULL,
            email VARCHAR NOT NULL,
            password_hash VARCHAR NOT NULL,
            name VARCHAR NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE,
            PRIMARY KEY (id),
            UNIQUE (email)
        )
    """))


def downgrade() -> None:
    op.drop_table("authorizations", if_exists=True)
