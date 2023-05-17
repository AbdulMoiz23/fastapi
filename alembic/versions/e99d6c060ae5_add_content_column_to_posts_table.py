"""add content column to posts table

Revision ID: e99d6c060ae5
Revises: 15fbab63b485
Create Date: 2023-04-03 14:08:46.254847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e99d6c060ae5'
down_revision = '15fbab63b485'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
