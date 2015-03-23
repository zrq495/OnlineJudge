# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sqlalchemy import sql
from sqlalchemy.ext.hybrid import hybrid_property

from oj import db
from .solution import SolutionModel


__all__ = [
    'ProblemModel',
    'ProblemStatisticsModel',
]


class ProblemModel(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    time_limit = db.Column(db.Integer)
    memory_limit = db.Column(db.Integer)
    description = db.Column(db.UnicodeText())
    input = db.Column(db.UnicodeText())
    output = db.Column(db.UnicodeText())
    sample_input = db.Column(db.UnicodeText())
    sample_output = db.Column(db.UnicodeText())
    sample_code = db.Column(db.UnicodeText())
    hint = db.Column(db.UnicodeText())
    source = db.Column(db.String(512))
    author = db.Column(db.String(128))
    is_display = db.Column(
        db.Boolean, default=True, server_default=sql.true(),
        nullable=True)
    is_special_judge = db.Column(
        db.Boolean, default=False, server_default=sql.false(),
        nullable=True)
    date_modified = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    _statistics = db.relationship(
        'ProblemStatisticsModel',
        primaryjoin='ProblemModel.id==ProblemStatisticsModel.id',
        foreign_keys='[ProblemStatisticsModel.id]',
        uselist=False,
        passive_deletes='all'
    )

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='SolutionModel.problem_id==ProblemModel.id',
        foreign_keys='[SolutionModel.problem_id]',
        backref=db.backref(
            'problem',
            lazy='joined',
            innerjoin=True),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    accepts = db.relationship(
        'SolutionModel',
        primaryjoin='and_(SolutionModel.problem_id==ProblemModel.id, SolutionModel.result==1)',
        foreign_keys='[SolutionModel.problem_id]',
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    solution_users = db.relationship(
        'UserModel',
        secondary=lambda: SolutionModel.__table__,
        primaryjoin='ProblemModel.id==SolutionModel.problem_id',
        secondaryjoin='UserModel.id==SolutionModel.user_id',
        order_by='SolutionModel.date_created.desc()',
        foreign_keys='[SolutionModel.user_id, SolutionModel.problem_id]',
        lazy='dynamic'
    )

    accept_users = db.relationship(
        'UserModel',
        secondary=lambda: SolutionModel.__table__,
        primaryjoin='and_(SolutionModel.problem_id==ProblemModel.id, SolutionModel.result==1)',
        secondaryjoin='UserModel.id==SolutionModel.user_id',
        order_by='SolutionModel.date_created.desc()',
        foreign_keys='[SolutionModel.user_id, SolutionModel.problem_id]',
        lazy='dynamic'
    )

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            p = ProblemModel(
                title=forgery_py.lorem_ipsum.title())
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @hybrid_property
    def solutions_count(self):
        if self._statistics:
            return self._statistics.solutions_count
        else:
            return 0

    @solutions_count.setter
    def solutions_count_setter(self, value):
        if not self._statistics:
            self._statistics = ProblemStatisticsModel()
        self._statistics.solutions_count = value

    @solutions_count.expression
    def solutions_count_expr(cls):
        return ProblemStatisticsModel.solutions_count

    @hybrid_property
    def accepts_count(self):
        if self._statistics:
            return self._statistics.accepts_count
        else:
            return 0

    @accepts_count.setter
    def accepts_count_setter(self, value):
        if not self._statistics:
            self._statistics = ProblemStatisticsModel()
        self._statistics.accepts_count = value

    @accepts_count.expression
    def accepts_count_expr(cls):
        return ProblemStatisticsModel.accepts_count

    @hybrid_property
    def solution_users_count(self):
        if self._statistics:
            return self._statistics.solution_users_count
        else:
            return 0

    @solution_users_count.setter
    def solution_users_count_setter(self, value):
        if not self._statistics:
            self._statistics = ProblemStatisticsModel()
        self._statistics.solution_users_count = value

    @solution_users_count.expression
    def solution_users_count_expr(cls):
        return ProblemStatisticsModel.solution_users_count

    @hybrid_property
    def accept_users_count(self):
        if self._statistics:
            return self._statistics.accept_users_count
        else:
            return 0

    @accept_users_count.setter
    def accept_users_count_setter(self, value):
        if not self._statistics:
            self._statistics = ProblemStatisticsModel()
        self._statistics.accept_users_count = value

    @accept_users_count.expression
    def accept_users_count_expr(cls):
        return ProblemStatisticsModel.accept_users_count

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Problem %r>' % self.title


class ProblemStatisticsModel(db.Model):
    __tablename__ = 'problem_statistics'

    id = db.Column(
        db.Integer(),
        nullable=False,
        primary_key=True,
        autoincrement=False)

    solutions_count = db.Column(
        db.Integer(), default=0,
        nullable=False, server_default='0', index=True)
    accepts_count = db.Column(
        db.Integer(), default=0,
        nullable=False, server_default='0', index=True)
    solution_users_count = db.Column(
        db.Integer(), default=0,
        nullable=False, server_default='0', index=True)
    accept_users_count = db.Column(
        db.Integer(), default=0,
        nullable=False, server_default='0', index=True)
