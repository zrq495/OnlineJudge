# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'SolutionModel',
]


class SolutionModel(db.Model):
    __tablename__ = 'solution'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    problem_id = db.Column(db.Integer(), nullable=False)
    contest_id = db.Column(db.Integer(), default=None)
    take_time = db.Column(db.Integer(), nullable=False)
    take_memory = db.Column(db.Integer(), nullable=False)
    code_length = db.Column(db.Integer(), nullable=False)
    program_language = db.Column(db.String(64), nullable=False)
    result = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<Solution %r>' % self.id
