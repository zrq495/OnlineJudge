"""alter problem AUTO_INCREMENT

Revision ID: 2a13a5f99959
Revises: 316d64ccd968
Create Date: 2015-06-12 10:39:07.790053

"""

# revision identifiers, used by Alembic.
revision = '2a13a5f99959'
down_revision = '316d64ccd968'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER SEQUENCE problem_id_seq RESTART WITH 1000;')


def downgrade():
    pass
