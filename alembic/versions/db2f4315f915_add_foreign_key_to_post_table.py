"""Add foreign key to post table

Revision ID: db2f4315f915
Revises: 7776893a8f0e
Create Date: 2026-11-10 12:52:31.387744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db2f4315f915'
down_revision: Union[str, Sequence[str], None] = '7776893a8f0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = True))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
