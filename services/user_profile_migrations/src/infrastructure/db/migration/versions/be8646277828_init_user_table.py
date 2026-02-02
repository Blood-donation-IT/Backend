"""init user table

Revision ID: be8646277828
Revises: 
Create Date: 2025-09-30 00:22:51.382432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'be8646277828'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS users_ (
            id BIGINT NOT NULL,
            email VARCHAR NOT NULL,
            password_hash VARCHAR NOT NULL,
            full_name VARCHAR NOT NULL,
            phone VARCHAR,
            blood_type VARCHAR,
            is_verified BOOLEAN NOT NULL,
            total_donations INTEGER NOT NULL,
            last_donation_at TIMESTAMP WITHOUT TIME ZONE,
            roles VARCHAR[] NOT NULL,
            is_active BOOLEAN NOT NULL,
            is_banned BOOLEAN NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE,
            PRIMARY KEY (id),
            UNIQUE (email),
            UNIQUE (phone)
        )
    """))


def downgrade() -> None:
    op.drop_table('users_', if_exists=True)
