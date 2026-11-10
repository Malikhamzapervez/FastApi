"""Create brand new column in post table

Revision ID: 9a9285578e87
Revises: d12580e5c3e2
Create Date: 2026-11-10 11:54:04.591375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a9285578e87'
down_revision: Union[str, Sequence[str], None] = 'd12580e5c3e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
