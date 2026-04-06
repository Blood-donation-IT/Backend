"""initial notifications table

Revision ID: 001_notifications_init
Revises:
Create Date: 2026-03-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_notifications_init"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS notifications (
            id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            title VARCHAR NOT NULL DEFAULT '',
            message VARCHAR NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            is_read BOOLEAN NOT NULL DEFAULT FALSE,
            type INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (id)
        )
    """))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_notifications_user_id ON notifications(user_id)"))


def downgrade() -> None:
    op.drop_table("notifications", if_exists=True)
