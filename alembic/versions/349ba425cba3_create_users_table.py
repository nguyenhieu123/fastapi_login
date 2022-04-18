"""create users table

Revision ID: 349ba425cba3
Revises: 
Create Date: 2022-04-15 08:39:57.300672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '349ba425cba3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer),
        sa.Column('user_name', sa.String),
        sa.Column('email', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
