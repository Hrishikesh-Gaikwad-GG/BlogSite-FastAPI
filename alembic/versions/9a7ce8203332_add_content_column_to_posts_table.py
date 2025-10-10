"""add content column to posts table

Revision ID: 9a7ce8203332
Revises: 0ff94503be65
Create Date: 2025-10-08 15:40:02.696045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a7ce8203332'
down_revision: Union[str, Sequence[str], None] = '0ff94503be65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
