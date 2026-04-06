"""initial applications table

Revision ID: 001_app_init
Revises:
Create Date: 2025-01-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_app_init"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Idempotent: create table only if it does not exist."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS applications (
            id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            blood_type VARCHAR NOT NULL,
            application_time TIMESTAMP WITH TIME ZONE NOT NULL,
            application_day TIMESTAMP WITH TIME ZONE,
            location_id VARCHAR,
            status VARCHAR NOT NULL DEFAULT 'pending',
            description VARCHAR,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE,
            PRIMARY KEY (id)
        )
    """))


def downgrade() -> None:
    op.drop_table("applications", if_exists=True)
