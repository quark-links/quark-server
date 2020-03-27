"""Add users table and foreign key.

Revision ID: 491e72874152
Revises: a23bc9910bcd
Create Date: 2020-03-22 19:50:18.055716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '491e72874152'
down_revision = 'a23bc9910bcd'
branch_labels = None
depends_on = None


def upgrade():
    """Apply updated schema to the database."""
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(timezone=True),
                              server_default=sa.text('(CURRENT_TIMESTAMP)'),
                              nullable=False),
                    sa.Column('updated', sa.DateTime(timezone=True),
                              server_default=sa.text('(CURRENT_TIMESTAMP)'),
                              onupdate=sa.text('(CURRENT_TIMESTAMP)'),
                              nullable=False),
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
    with op.batch_alter_table('shortlink', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])


def downgrade():
    """Undo schema changes."""
    with op.batch_alter_table('shortlink', schema=None) as batch_op:
        batch_op.drop_constraint("fk_shortlink_user_id_user",
                                 type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_table('user')
