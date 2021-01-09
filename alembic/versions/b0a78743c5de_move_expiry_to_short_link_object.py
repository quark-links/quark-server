"""Move expiry to short link object.

Revision ID: b0a78743c5de
Revises: bce812ae17b3
Create Date: 2021-01-09 17:52:38.498228
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0a78743c5de'
down_revision = 'bce812ae17b3'
branch_labels = None
depends_on = None


# Create two simple tables with the columns that we are using/changing
upload_table = sa.Table(
    'upload',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('short_link_id', sa.Integer, sa.ForeignKey("shortlink.id")),
    sa.Column('expires', sa.DateTime(timezone=True), nullable=False)
)

short_link_table = sa.Table(
    'shortlink',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('expiry', sa.DateTime(timezone=True), nullable=True)
)


def upgrade():
    """Upgrade the database from the previous version."""
    # Create the new expiry column
    with op.batch_alter_table('shortlink', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiry', sa.DateTime(timezone=True),
                            nullable=True))

    # Copy from the old expires column into the new expiry column
    conn = op.get_bind()
    for upload in conn.execute(upload_table.select()):
        conn.execute(short_link_table.update().where(
            short_link_table.c.id == upload.short_link_id
        ).values(
            expiry=upload.expires
        ))

    # Delete the old expires column
    with op.batch_alter_table('upload', schema=None) as batch_op:
        batch_op.drop_column('expires')


def downgrade():
    """Downgrade the database to the previous version."""
    # Create the old expires column
    with op.batch_alter_table('upload', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expires', sa.DATETIME(),
                            nullable=True))

    # Copy from the new expires column into the old expiry column
    conn = op.get_bind()
    for upload in conn.execute(upload_table.select()):
        shortlink = conn.execute(short_link_table.select().where(
            short_link_table.c.id == upload.short_link_id)).fetchone()

        conn.execute(upload_table.update().where(
            upload_table.c.id == upload.id
        ).values(
            expires=shortlink.expiry
        ))

    # Delete the new expiry column
    with op.batch_alter_table('shortlink', schema=None) as batch_op:
        batch_op.drop_column('expiry')
