"""add last few columns to the posts table

Revision ID: 975e33ab1649
Revises: 70e630a5285a
Create Date: 2025-10-08 16:13:02.090264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '975e33ab1649'
down_revision: Union[str, Sequence[str], None] = '70e630a5285a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable =  False, server_default= 'TRUE'
    ))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone= True), nullable = False, server_default= sa.text('NOW()')
    ))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
