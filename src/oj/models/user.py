# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sqlalchemy.ext.hybrid import hybrid_property

from oj import db


__all__ = [
    'UserModel',
    'UserStatisticsModel',
]


@db.preserve_deleted(
    date_deleted=db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False,
        index=True))
class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, index=True)
    nickname = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    school = db.Column(db.String(256))
    program_language = db.Column(db.String(64))
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    _statistics = db.relationship(
        'UserStatisticsModel',
        primaryjoin='UserModel.id==UserStatisticsModel.id',
        foreign_keys='[UserStatisticsModel.id]',
        uselist=False,
        passive_deletes='all')

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='SolutionModel.user_id==UserModel.id',
        foreign_keys='[SolutionModel.user_id]',
        backref=db.backref(
            'user',
            lazy='joined',
            innerjoin=True),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    @hybrid_property
    def solutions_count(self):
        if self._statistics:
            return self._statistics.solutions_count
        else:
            return 0

    @solutions_count.setter
    def solutions_count_setter(self, value):
        if not self._statistics:
            self._statistics = UserStatisticsModel()
        self._statistics.solutions_count = value

    @solutions_count.expression
    def solutions_count_expr(cls):
        return UserStatisticsModel.solutions_count

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def __repr__(self):
        return '<User %r>' % self.username


class UserStatisticsModel(db.Model):
    __tablename__ = 'user_statistics'

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
