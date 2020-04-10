"""Create user API key.

Revision ID: 84b5024e6a1e
Revises: eb4eda067153
Create Date: 2020-04-05 12:03:38.494401
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '84b5024e6a1e'
down_revision = 'eb4eda067153'
branch_labels = None
depends_on = None


def upgrade():
    """Apply updated schema to the database."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('api_key', sa.String(length=100),
                                      nullable=True))


def downgrade():
    """Undo schema changes."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('api_key')
