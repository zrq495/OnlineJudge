# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'ProblemModel',
]


class ProblemModel(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), unique=True, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Problem %r>' % self.title
