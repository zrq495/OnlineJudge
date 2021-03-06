"""empty message

Revision ID: 4c38b5b7dfe5
Revises: 4dd00a9bd420
Create Date: 2015-04-09 18:00:02.867355

"""

# revision identifiers, used by Alembic.
revision = '4c38b5b7dfe5'
down_revision = '4dd00a9bd420'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('solution', sa.Column('contest_user_id', sa.Integer(), nullable=True))
    op.alter_column('solution', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('solution', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('solution', 'contest_user_id')
    ### end Alembic commands ###
