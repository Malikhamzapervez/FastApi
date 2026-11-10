"""User table

Revision ID: 7776893a8f0e
Revises: 9a9285578e87
Create Date: 2026-11-10 12:12:36.768674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7776893a8f0e'
down_revision: Union[str, Sequence[str], None] = '9a9285578e87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(), nullable = False),
                    sa.Column('email',sa.String(), nullable = False),
                    sa.Column('password',sa.String(), nullable = False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone = True),
                                server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
