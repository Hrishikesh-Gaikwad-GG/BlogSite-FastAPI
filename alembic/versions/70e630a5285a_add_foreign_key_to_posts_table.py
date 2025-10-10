"""add foreign-key to posts table

Revision ID: 70e630a5285a
Revises: cb0ac35608d0
Create Date: 2025-10-08 16:03:48.507425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70e630a5285a'
down_revision: Union[str, Sequence[str], None] = 'cb0ac35608d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_users_fk', source_table = 'posts', referent_table = 'users',
                          local_cols= ['owner_id'], remote_cols = ['id'], ondelete= 'CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name= 'posts')
    op.drop_column('posts', 'owner_id')
    pass
