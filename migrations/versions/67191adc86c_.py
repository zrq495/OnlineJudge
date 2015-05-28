"""empty message

Revision ID: 67191adc86c
Revises: 4c943b7423d3
Create Date: 2015-03-22 12:24:22.636733

"""

# revision identifiers, used by Alembic.
revision = '67191adc86c'
down_revision = '4c943b7423d3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('solution', 'contest_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('solution', 'contest_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    ### end Alembic commands ###