"""user confirm

Revision ID: 3211fb10978c
Revises: 2a13a5f99959
Create Date: 2015-10-14 19:51:31.981780

"""

# revision identifiers, used by Alembic.
revision = '3211fb10978c'
down_revision = '2a13a5f99959'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), server_default=sa.text(u'false'), nullable=False))
    op.add_column('user_deleted', sa.Column('confirmed', sa.Boolean(), server_default=sa.text(u'false'), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_deleted', 'confirmed')
    op.drop_column('user', 'confirmed')
    ### end Alembic commands ###
