"""add slot_index to applications

Revision ID: 002_slot_index
Revises: 001_app_init
Create Date: 2025-04-06

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002_slot_index"
down_revision: Union[str, Sequence[str], None] = "001_app_init"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Idempotent: add column only if it does not exist."""
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            ALTER TABLE applications
            ADD COLUMN IF NOT EXISTS slot_index INTEGER
            """
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE applications DROP COLUMN IF EXISTS slot_index"))
