"""Remove user username.

Revision ID: 1ff078c1cafb
Revises: b63f3bbf25f0
Create Date: 2020-10-25 10:58:41.276530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ff078c1cafb'
down_revision = 'b63f3bbf25f0'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database from the previous version."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50),
                                      nullable=True))
        batch_op.drop_constraint('uq_user_username', type_='unique')
        batch_op.drop_column('username')


def downgrade():
    """Downgrade the database to the previous version."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=50),
                                      nullable=False))
        batch_op.create_unique_constraint('uq_user_username', ['username'])
        batch_op.drop_column('name')
