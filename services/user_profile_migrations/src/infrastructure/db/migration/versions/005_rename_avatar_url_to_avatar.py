"""rename users_.avatar_url to avatar

Revision ID: 005_avatar
Revises: 004_health_test
Create Date: 2026-04-28
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005_avatar"
down_revision: Union[str, Sequence[str], None] = "004_health_test"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'users_' AND column_name = 'avatar_url'
                ) AND NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'users_' AND column_name = 'avatar'
                ) THEN
                    ALTER TABLE users_ RENAME COLUMN avatar_url TO avatar;
                END IF;
            END $$;
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'users_' AND column_name = 'avatar'
                ) AND NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'users_' AND column_name = 'avatar_url'
                ) THEN
                    ALTER TABLE users_ RENAME COLUMN avatar TO avatar_url;
                END IF;
            END $$;
            """
        )
    )
