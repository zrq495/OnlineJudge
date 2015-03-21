# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'MessageModel',
]


class MessageModel(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer(), nullable=False)
    to_user_id = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(512), nullable=False)
    content = db.Column(db.UnicodeText(), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Message %r>' % self.title
