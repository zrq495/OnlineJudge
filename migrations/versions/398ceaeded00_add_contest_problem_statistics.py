"""add contest problem statistics

Revision ID: 398ceaeded00
Revises: aa4c9d8bbdf
Create Date: 2015-04-25 10:14:12.139760

"""

# revision identifiers, used by Alembic.
revision = '398ceaeded00'
down_revision = 'aa4c9d8bbdf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contest_problem_statistics',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('solutions_count', sa.Integer(), server_default=u'0', nullable=False),
    sa.Column('accepts_count', sa.Integer(), server_default=u'0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contest_problem_statistics_accepts_count'), 'contest_problem_statistics', ['accepts_count'], unique=False)
    op.create_index(op.f('ix_contest_problem_statistics_solutions_count'), 'contest_problem_statistics', ['solutions_count'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contest_problem_statistics_solutions_count'), table_name='contest_problem_statistics')
    op.drop_index(op.f('ix_contest_problem_statistics_accepts_count'), table_name='contest_problem_statistics')
    op.drop_table('contest_problem_statistics')
    ### end Alembic commands ###
