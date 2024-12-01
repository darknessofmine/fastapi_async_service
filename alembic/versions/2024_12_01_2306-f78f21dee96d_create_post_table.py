"""create post table

Revision ID: f78f21dee96d
Revises: 768f9fa625ea
Create Date: 2024-12-01 23:06:33.896010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f78f21dee96d'
down_revision: Union[str, None] = '768f9fa625ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'posts',
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('text', sa.Text(), server_default='', nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###