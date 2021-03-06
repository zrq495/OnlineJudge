"""add registry model

Revision ID: 1f8b42b9327d
Revises: 3c8de56eeebc
Create Date: 2015-05-24 14:50:30.254262

"""

# revision identifiers, used by Alembic.
revision = '1f8b42b9327d'
down_revision = '3c8de56eeebc'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registry',
    sa.Column('key', sa.String(length=100), nullable=False),
    sa.Column('name', sa.Unicode(length=1024), nullable=False),
    sa.Column('meta', postgresql.JSON(), nullable=False),
    sa.Column('value', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registry')
    ### end Alembic commands ###
