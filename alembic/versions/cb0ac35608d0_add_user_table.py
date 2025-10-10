"""add user table

Revision ID: cb0ac35608d0
Revises: 9a7ce8203332
Create Date: 2025-10-08 15:48:08.486798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb0ac35608d0'
down_revision: Union[str, Sequence[str], None] = '9a7ce8203332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True),
                              server_default= sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
