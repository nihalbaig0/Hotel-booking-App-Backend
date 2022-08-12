"""add content column to posts table

Revision ID: 3c76804a8ee0
Revises: 7b9d4e722e83
Create Date: 2022-04-29 16:28:11.144928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c76804a8ee0'
down_revision = '7b9d4e722e83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
