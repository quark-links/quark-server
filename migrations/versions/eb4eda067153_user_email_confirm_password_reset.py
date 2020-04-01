"""Add user email confirmation and password reset columns.

Revision ID: eb4eda067153
Revises: 491e72874152
Create Date: 2020-03-29 11:01:19.489292
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb4eda067153'
down_revision = '491e72874152'
branch_labels = None
depends_on = None


def upgrade():
    """Apply updated schema to the database."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(),
                                      nullable=False, default=False))
        batch_op.add_column(sa.Column('confirmed_on',
                                      sa.DateTime(timezone=True),
                                      nullable=True))
        batch_op.add_column(sa.Column('confirm_token',
                                      sa.String(20),
                                      nullable=True))
        batch_op.add_column(sa.Column('reset_token',
                                      sa.String(20),
                                      nullable=True))


def downgrade():
    """Undo schema changes."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('confirmed_on')
        batch_op.drop_column('confirmed')
        batch_op.drop_column('confirm_token')
        batch_op.drop_column('reset_token')
