"""Initial database schema.

Revision ID: da3f9b349c7b
Revises:
Create Date: 2020-01-18 17:39:11.081118
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da3f9b349c7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply updated schema to the database."""
    op.create_table('shortlink',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(timezone=True),
                              server_default=sa.text('(CURRENT_TIMESTAMP)'),
                              nullable=True),
                    sa.Column('updated', sa.DateTime(timezone=True),
                              server_default=sa.text('(CURRENT_TIMESTAMP)'),
                              nullable=True),
                    sa.Column('creator_ip', sa.String(length=50),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('paste',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('short_link_id', sa.Integer(), nullable=True),
                    sa.Column('language', sa.String(length=100),
                              nullable=False),
                    sa.Column('code', sa.TEXT(), nullable=False),
                    sa.Column('hash', sa.String(length=64), nullable=False),
                    sa.ForeignKeyConstraint(['short_link_id'],
                                            ['shortlink.id']),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('upload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('short_link_id', sa.Integer(), nullable=True),
                    sa.Column('mimetype', sa.String(length=100),
                              nullable=False),
                    sa.Column('original_filename', sa.String(length=400),
                              nullable=False),
                    sa.Column('filename', sa.String(length=400),
                              nullable=True),
                    sa.Column('hash', sa.String(length=64), nullable=False),
                    sa.Column('expires', sa.DateTime(timezone=True),
                              nullable=False),
                    sa.ForeignKeyConstraint(['short_link_id'],
                                            ['shortlink.id']),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('url',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('short_link_id', sa.Integer(), nullable=True),
                    sa.Column('url', sa.String(length=2048), nullable=False),
                    sa.ForeignKeyConstraint(['short_link_id'],
                                            ['shortlink.id']),
                    sa.PrimaryKeyConstraint('id'))


def downgrade():
    """Undo schema changes."""
    op.drop_table('url')
    op.drop_table('upload')
    op.drop_table('paste')
    op.drop_table('shortlink')
