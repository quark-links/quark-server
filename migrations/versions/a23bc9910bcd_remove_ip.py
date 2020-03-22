"""Remove IP address column.

Revision ID: a23bc9910bcd
Revises: da3f9b349c7b
Create Date: 2020-03-17 09:09:48.919247
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a23bc9910bcd'
down_revision = 'da3f9b349c7b'
branch_labels = None
depends_on = None


def upgrade():
    """Apply updated schema to the database."""
    with op.batch_alter_table("shortlink") as batch_op:
        batch_op.drop_column("creator_ip")


def downgrade():
    """Undo schema changes."""
    op.add_column('shortlink', sa.Column('creator_ip',
                                         sa.String(50),
                                         nullable=True))
