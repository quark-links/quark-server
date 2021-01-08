"""Remove unnecessary fields.

Revision ID: b63f3bbf25f0
Revises: 84b5024e6a1e
Create Date: 2020-10-22 19:22:21.486624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b63f3bbf25f0'
down_revision = '84b5024e6a1e'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database from the previous version."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('authenticated')


def downgrade():
    """Downgrade the database to the previous version."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('authenticated', sa.BOOLEAN(),
                                      nullable=False, server_default="0"))
