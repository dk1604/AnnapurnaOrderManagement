"""create initial tables

Revision ID: V1
Revises: 
Create Date: 2024-12-23 12:55:21.293724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'V1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('canteen_alembic_version',
    sa.Column('version_num', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('version_num')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), nullable=True),
    sa.Column('description', sa.VARCHAR(length=250), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu')
    op.drop_table('canteen_alembic_version')
    # ### end Alembic commands ###
