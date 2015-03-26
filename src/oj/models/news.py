# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import url_for
from sqlalchemy import sql

from oj import db
from .user import UserModel


__all__ = [
    'NewsModel',
]


class NewsModel(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(512), nullable=False)
    content = db.Column(db.UnicodeText(), nullable=False)
    is_display = db.Column(
        db.Boolean, default=True, server_default=sql.true(),
        nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    @property
    def url(self):
        return url_for('news.detail', news_id=self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        user_count = UserModel.query.count()
        if user_count == 0:
            UserModel.generate_fake()
            user_count = UserModel.query.count()
        for i in range(count):
            u = UserModel.query.offset(randint(0, user_count - 1)).first()
            n = NewsModel(
                user_id=u.id,
                title=forgery_py.lorem_ipsum.title(),
                content=forgery_py.lorem_ipsum.paragraphs())
            db.session.add(n)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<News %r>' % self.title
