"""add headline model

Revision ID: 2563b1147545
Revises: 398ceaeded00
Create Date: 2015-04-25 19:08:12.711034

"""

# revision identifiers, used by Alembic.
revision = '2563b1147545'
down_revision = '398ceaeded00'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('headline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(length=512), nullable=False),
    sa.Column('url', sa.Unicode(length=512), nullable=True),
    sa.Column('alert', sa.Enum(u'info', u'success', u'warning', u'danger', name='headline_alert_enum'), server_default=u'info', nullable=False),
    sa.Column('is_display', sa.Boolean(), server_default=sa.text(u'true'), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_headline_date_created'), 'headline', ['date_created'], unique=False)
    op.create_index(op.f('ix_headline_is_display'), 'headline', ['is_display'], unique=False)
    op.create_index(op.f('ix_headline_user_id'), 'headline', ['user_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_headline_user_id'), table_name='headline')
    op.drop_index(op.f('ix_headline_is_display'), table_name='headline')
    op.drop_index(op.f('ix_headline_date_created'), table_name='headline')
    op.drop_table('headline')
    ### end Alembic commands ###
