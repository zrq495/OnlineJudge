# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'ProblemModel',
]


class ProblemModel(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

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

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Problem %r>' % self.title
