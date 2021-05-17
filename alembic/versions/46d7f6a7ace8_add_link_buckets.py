"""Add link buckets.

Revision ID: 46d7f6a7ace8
Revises: 452e0a651241
Create Date: 2021-05-17 18:40:24.703877
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46d7f6a7ace8'
down_revision = '452e0a651241'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database from the previous version."""
    op.create_table('bucket',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.String(length=500),
                              nullable=True),
                    sa.Column('public', sa.Boolean(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'],
                        name=op.f('fk_bucket_user_id_user')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_bucket')))

    with op.batch_alter_table('shortlink', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bucket_id', sa.Integer(),
                                      nullable=True))
        batch_op.create_foreign_key(
            batch_op.f('fk_shortlink_bucket_id_bucket'), 'bucket',
            ['bucket_id'], ['id'])


def downgrade():
    """Downgrade the database to the previous version."""
    with op.batch_alter_table('shortlink', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_shortlink_bucket_id_bucket'),
                                 type_='foreignkey')
        batch_op.drop_column('bucket_id')

    op.drop_table('bucket')
