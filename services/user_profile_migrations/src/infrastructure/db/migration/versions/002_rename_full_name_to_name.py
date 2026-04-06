"""rename full_name to name

Revision ID: 002_name
Revises: be8646277828
Create Date: 2025-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002_name"
down_revision: Union[str, Sequence[str], None] = "be8646277828"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = 'users_' AND column_name = 'full_name'
            ) THEN
                ALTER TABLE users_ RENAME COLUMN full_name TO name;
            END IF;
        END $$;
        """
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = 'users_' AND column_name = 'name'
            ) THEN
                ALTER TABLE users_ RENAME COLUMN name TO full_name;
            END IF;
        END $$;
        """
        )
    )
