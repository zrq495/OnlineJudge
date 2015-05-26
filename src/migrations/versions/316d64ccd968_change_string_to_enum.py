"""change string to enum

Revision ID: 316d64ccd968
Revises: 299d5e302ccd
Create Date: 2015-05-26 11:35:36.897434

"""

# revision identifiers, used by Alembic.
revision = '316d64ccd968'
down_revision = '299d5e302ccd'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


def upgrade():
    ENUM(u'gcc', u'g++', u'java', name=u'user_program_language_enum').create(op.get_bind(), checkfirst=False)
    op.alter_column('user', 'program_language', existing_type=sa.Enum(u'gcc', u'g++', u'java', name=u'user_program_language_enum'), nullable=True)
    op.alter_column('user_deleted', 'program_language', existing_type=sa.Enum(u'male', u'female', name='user_gender'), nullable=True)

    ENUM(u'gcc', u'g++', u'java', name=u'solution_program_language_enum').create(op.get_bind(), checkfirst=False)
    op.alter_column('solution', 'program_language', existing_type=sa.Enum(u'gcc', u'g++', u'java', name=u'solution_program_language_enum'), nullable=False)


def downgrade():
    op.alter_column('user', 'program_language',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('user_deleted', 'program_language',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('solution', 'program_language',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    ENUM(name=u'user_program_language_enum').drop(op.get_bind(), checkfirst=False)
    ENUM(name=u'solution_program_language_enum').drop(op.get_bind(), checkfirst=False)
