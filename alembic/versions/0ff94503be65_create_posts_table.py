"""create posts table

Revision ID: 0ff94503be65
Revises: 
Create Date: 2025-10-08 15:21:43.580201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ff94503be65'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                                       sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('posts')
    pass