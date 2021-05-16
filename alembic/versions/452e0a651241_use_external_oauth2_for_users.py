"""Use external OAuth2 for users.

Revision ID: 452e0a651241
Revises: b0a78743c5de
Create Date: 2021-05-16 16:35:12.349256
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '452e0a651241'
down_revision = 'b0a78743c5de'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database from the previous version."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sub', sa.String(length=100),
                                      nullable=True))
        batch_op.drop_constraint('uq_user_email', type_='unique')
        batch_op.drop_column('active')
        batch_op.drop_column('email')
        batch_op.drop_column('confirm_token')
        batch_op.drop_column('name')
        batch_op.drop_column('reset_token')
        batch_op.drop_column('confirmed')
        batch_op.drop_column('api_key')
        batch_op.drop_column('confirmed_on')
        batch_op.drop_column('password')


def downgrade():
    """Downgrade the database to the previous version."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=400),
                                      nullable=False))
        batch_op.add_column(sa.Column('confirmed_on', sa.DATETIME(),
                                      nullable=True))
        batch_op.add_column(sa.Column('api_key', sa.VARCHAR(length=100),
                                      nullable=True))
        batch_op.add_column(sa.Column('confirmed', sa.BOOLEAN(),
                                      nullable=False))
        batch_op.add_column(sa.Column('reset_token', sa.VARCHAR(length=100),
                                      nullable=True))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50),
                                      nullable=True))
        batch_op.add_column(sa.Column('confirm_token', sa.VARCHAR(length=100),
                                      nullable=True))
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=100),
                                      nullable=True))
        batch_op.add_column(sa.Column('active', sa.BOOLEAN(),
                                      nullable=False))
        batch_op.create_unique_constraint('uq_user_email', ['email'])
        batch_op.drop_column('sub')
