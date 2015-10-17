"""remove alert from headline

Revision ID: 4e5ac0ad1a5d
Revises: 3211fb10978c
Create Date: 2015-10-17 15:18:15.847360

"""

# revision identifiers, used by Alembic.
revision = '4e5ac0ad1a5d'
down_revision = '3211fb10978c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('headline', 'alert')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('headline', sa.Column('alert', postgresql.ENUM(u'info', u'success', u'warning', u'danger', name='headline_alert_enum'), server_default=sa.text(u"'info'::headline_alert_enum"), autoincrement=False, nullable=False))
    ### end Alembic commands ###