"""create users table

Revision ID: da33ff3abe1e
Revises: 
Create Date: 2025-09-04 07:56:22.928617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da33ff3abe1e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users_',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('phone', sa.String, nullable=True),
        sa.Column('blood_type', sa.String, nullable=True),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('total_donations', sa.Integer, default=0),
        sa.Column('last_donation_at', sa.DateTime, nullable=True),
        sa.Column('roles', sa.ARRAY(sa.String), default=[]),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_banned', sa.Boolean, default=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users_')
