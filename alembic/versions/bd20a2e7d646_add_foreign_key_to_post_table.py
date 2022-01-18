"""add foreign key to post table

Revision ID: bd20a2e7d646
Revises: 19c24614d932
Create Date: 2022-01-18 09:45:59.410212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd20a2e7d646'
down_revision = '19c24614d932'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_Users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],
                          remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_Users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
