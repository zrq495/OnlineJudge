# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sqlalchemy.sql import expression
from sqlalchemy import sql

from oj import db


__all__ = [
    'MessageModel',
]


class MessageModel(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer(), nullable=False, index=True)
    to_user_id = db.Column(db.Integer(), nullable=False, index=True)
    title = db.Column(db.String(512), nullable=False)
    content = db.Column(db.UnicodeText(), nullable=False)
    is_read = db.Column(db.Boolean(), server_default=sql.false(),
                        nullable=False, index=True)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    @staticmethod
    def get_unread_count(user_id):
        return MessageModel.query.filter(
            MessageModel.to_user_id == user_id,
            MessageModel.is_read.is_(False),
        ).count()

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Message %r>' % self.title
