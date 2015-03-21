# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'ContestModel',
    'ContestProblemModel',
]


class ContestModel(db.Model):
    __tablename__ = 'contest'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='SolutionModel.contest_id==ContestModel.id',
        foreign_keys='[SolutionModel.contest_id]',
        backref=db.backref(
            'contest',
            lazy='joined',
            innerjoin=True),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    problems = db.relationship(
        'ContestProblemModel',
        primaryjoin='ContestProblemModel.contest_id==ContestModel.id',
        foreign_keys='[ContestProblemModel.contest_id]',
        backref=db.backref(
            'contest',
            lazy='joined',
            innerjoin=True),
        order_by='ContestProblemModel.ordinal.asc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Contest %r>' % self.title


class ContestProblemModel(db.Model):
    __tablename__ = 'contest_problem'

    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer(), nullable=False)
    problem_id = db.Column(db.Integer(), nullable=False)
    ordinal = db.Column(db.Integer(), default=0)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    problem = db.relationship(
        'ProblemModel',
        primaryjoin='ProblemModel.id==ContestProblemModel.problem_id',
        foreign_keys='[ContestProblemModel.problem_id]',
        uselist=False
    )

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<ContestProblem %r>' % self.id
