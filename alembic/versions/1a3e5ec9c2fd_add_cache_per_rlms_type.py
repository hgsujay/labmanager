"""Add cache per rlms type

Revision ID: 1a3e5ec9c2fd
Revises: 7f806cb0445
Create Date: 2015-05-06 16:33:34.158433

"""

# revision identifiers, used by Alembic.
revision = '1a3e5ec9c2fd'
down_revision = '7f806cb0445'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rlmstype_cache',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('rlms_type', sa.Unicode(length=255), nullable=False),
    sa.Column('key', sa.Unicode(length=255), nullable=True),
    sa.Column('value', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(u'ix_rlmstype_cache_key', 'rlmstype_cache', ['key'], unique=False)
    op.create_index(u'ix_rlmstype_cache_rlms_type', 'rlmstype_cache', ['rlms_type'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(u'ix_rlmstype_cache_rlms_type', table_name='rlmstype_cache')
    op.drop_index(u'ix_rlmstype_cache_key', table_name='rlmstype_cache')
    op.drop_table('rlmstype_cache')
    ### end Alembic commands ###
