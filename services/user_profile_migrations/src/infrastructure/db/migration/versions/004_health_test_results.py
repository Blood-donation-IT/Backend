"""health_test_results table for donor screening + blood type

Revision ID: 004_health_test
Revises: 003_columns
Create Date: 2026-02-11

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004_health_test"
down_revision: Union[str, Sequence[str], None] = "003_columns"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
        CREATE TABLE IF NOT EXISTS health_test_results (
            user_id BIGINT NOT NULL PRIMARY KEY
                REFERENCES users_(id) ON DELETE CASCADE,
            completed_at TIMESTAMP WITH TIME ZONE NOT NULL,
            q1 BOOLEAN NOT NULL,
            q2 BOOLEAN NOT NULL,
            q3 BOOLEAN NOT NULL,
            q4 BOOLEAN NOT NULL,
            q5 BOOLEAN NOT NULL,
            q6 BOOLEAN NOT NULL,
            blood_type VARCHAR,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
        )
        """
        )
    )


def downgrade() -> None:
    op.drop_table("health_test_results")
