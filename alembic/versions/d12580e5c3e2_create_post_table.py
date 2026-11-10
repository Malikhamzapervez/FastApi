"""Create post table

Revision ID: d12580e5c3e2
Revises: 
Create Date: 2026-11-10 11:01:13.203680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd12580e5c3e2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable = False, primary_key = True)
                    , sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts')
    pass
