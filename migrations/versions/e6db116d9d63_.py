"""Add users table and foreign key.

Revision ID: e6db116d9d63
Revises: a23bc9910bcd
Create Date: 2020-03-22 14:32:23.479328
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6db116d9d63'
down_revision = 'a23bc9910bcd'
branch_labels = None
depends_on = None


def upgrade():
    """Apply updated schema to the database."""
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=True),
                    sa.Column('username', sa.String(length=50),
                              nullable=False),
                    sa.Column('password', sa.String(length=400),
                              nullable=False),
                    sa.Column('authenticated', sa.Boolean(), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username'))
    op.add_column('shortlink', sa.Column('user_id', sa.Integer(),
                                         nullable=True))
    op.create_foreign_key(None, 'shortlink', 'user', ['user_id'], ['id'])


def downgrade():
    """Undo schema changes."""
    op.drop_constraint(None, 'shortlink', type_='foreignkey')
    op.drop_column('shortlink', 'user_id')
    op.drop_table('user')
