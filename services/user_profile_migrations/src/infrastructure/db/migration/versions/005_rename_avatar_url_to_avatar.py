"""rename users_.avatar_url -> avatar

Revision ID: 005_avatar
Revises: 004_health_test
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005_avatar"
down_revision: Union[str, Sequence[str], None] = "004_health_test"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("ALTER TABLE users_ RENAME COLUMN avatar_url TO avatar"))


def downgrade() -> None:
    op.execute(sa.text("ALTER TABLE users_ RENAME COLUMN avatar TO avatar_url"))
