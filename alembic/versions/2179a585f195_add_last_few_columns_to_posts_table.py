"""add last few columns to posts table

Revision ID: 2179a585f195
Revises: 37a3ee1285a6
Create Date: 2023-04-03 17:25:23.900657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2179a585f195'
down_revision = '37a3ee1285a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                      server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
