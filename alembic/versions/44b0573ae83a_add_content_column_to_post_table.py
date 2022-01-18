"""add content column to post table

Revision ID: 44b0573ae83a
Revises: 560c438760b2
Create Date: 2022-01-18 09:35:49.812795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44b0573ae83a'
down_revision = '560c438760b2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
