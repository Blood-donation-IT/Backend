"""add avatar_url, lives_saved_count, donor_status, has_donor_book, test_is_done, birth_date

Revision ID: 003_columns
Revises: 002_name
Create Date: 2025-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003_columns"
down_revision: Union[str, Sequence[str], None] = "002_name"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE users_ ADD COLUMN IF NOT EXISTS avatar_url VARCHAR"))
    conn.execute(sa.text("ALTER TABLE users_ ADD COLUMN IF NOT EXISTS lives_saved_count INTEGER DEFAULT 0"))
    conn.execute(sa.text("ALTER TABLE users_ ADD COLUMN IF NOT EXISTS donor_status VARCHAR"))
    conn.execute(sa.text("ALTER TABLE users_ ADD COLUMN IF NOT EXISTS has_donor_book BOOLEAN DEFAULT false"))
    conn.execute(sa.text("ALTER TABLE users_ ADD COLUMN IF NOT EXISTS test_is_done BOOLEAN DEFAULT false"))
    conn.execute(sa.text("ALTER TABLE users_ ADD COLUMN IF NOT EXISTS birth_date TIMESTAMP WITH TIME ZONE"))


def downgrade() -> None:
    conn = op.get_bind()
    for col in ("birth_date", "test_is_done", "has_donor_book", "donor_status", "lives_saved_count", "avatar_url"):
        conn.execute(sa.text(f"ALTER TABLE users_ DROP COLUMN IF EXISTS {col}"))
