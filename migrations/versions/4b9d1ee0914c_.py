"""empty message

Revision ID: 4b9d1ee0914c
Revises: 67191adc86c
Create Date: 2015-03-22 12:56:42.723773

"""

# revision identifiers, used by Alembic.
revision = '4b9d1ee0914c'
down_revision = '67191adc86c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('problem_statistics', sa.Column('accept_users_count', sa.Integer(), server_default=u'0', nullable=False))
    op.add_column('problem_statistics', sa.Column('solution_users_count', sa.Integer(), server_default=u'0', nullable=False))
    op.create_index(op.f('ix_problem_statistics_accept_users_count'), 'problem_statistics', ['accept_users_count'], unique=False)
    op.create_index(op.f('ix_problem_statistics_solution_users_count'), 'problem_statistics', ['solution_users_count'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_problem_statistics_solution_users_count'), table_name='problem_statistics')
    op.drop_index(op.f('ix_problem_statistics_accept_users_count'), table_name='problem_statistics')
    op.drop_column('problem_statistics', 'solution_users_count')
    op.drop_column('problem_statistics', 'accept_users_count')
    ### end Alembic commands ###
