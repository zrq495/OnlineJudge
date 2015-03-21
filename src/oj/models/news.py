# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'NewsModel',
]


class NewsModel(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(512), nullable=False)
    content = db.Column(db.UnicodeText(), nullable=False)
    display = db.Column(db.Boolean, default=True)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<News %r>' % self.title
