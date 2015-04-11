# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from oj import db


__all__ = [
    'UserModel',
    'UserFavoritesModel',
    'UserStatisticsModel',
]


@db.preserve_deleted(
    id=db.Column(db.Integer,
                 primary_key=True,
                 nullable=False,
                 autoincrement=False),
    date_deleted=db.Column(db.DateTime,
                           nullable=False,
                           index=True,
                           server_default=db.func.current_timestamp()),
    reason=db.Column(db.Enum('deleted_by_user',
                             'deleted_by_admin',
                             'censored_automatically',
                             name='deleted_reason'),
                     nullable=False))
class UserModel(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, index=True, nullable=False)
    nickname = db.Column(db.String(256), unique=True, index=True, nullable=False)
    email = db.Column(db.String(256), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    gender = db.Column(
        db.Enum('male', 'female', name='user_gender'))
    school = db.Column(db.String(256))
    program_language = db.Column(db.String(64), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    _statistics = db.relationship(
        'UserStatisticsModel',
        primaryjoin='UserModel.id==UserStatisticsModel.id',
        foreign_keys='[UserStatisticsModel.id]',
        backref='user',
        uselist=False,
        cascade="all, delete-orphan",
    )

    favorites = db.relationship(
        'ProblemModel',
        secondary=lambda: UserFavoritesModel.__table__,
        primaryjoin='UserModel.id==UserFavoritesModel.user_id',
        secondaryjoin='ProblemModel.id==UserFavoritesModel.problem_id',
        order_by='UserFavoritesModel.date_created.desc()',
        foreign_keys='[UserFavoritesModel.problem_id, UserFavoritesModel.user_id]',
        lazy='dynamic'
    )

    message_sent = db.relationship(
        'MessageModel',
        primaryjoin='MessageModel.from_user_id==UserModel.id',
        foreign_keys='[MessageModel.from_user_id]',
        backref=db.backref(
            'user',
            lazy=True,
            uselist=False),
        order_by='MessageModel.date_created.desc()',
        lazy='dynamic'
    )

    message_received = db.relationship(
        'MessageModel',
        primaryjoin='MessageModel.to_user_id==UserModel.id',
        foreign_keys='[MessageModel.to_user_id]',
        order_by='MessageModel.date_created.desc()',
        lazy='dynamic'
    )

    news = db.relationship(
        'NewsModel',
        primaryjoin='NewsModel.user_id==UserModel.id',
        foreign_keys='[NewsModel.user_id]',
        backref=db.backref(
            'user',
            lazy=True,
            uselist=False),
        order_by='NewsModel.date_created.desc()',
        lazy='dynamic'
    )

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='SolutionModel.user_id==UserModel.id',
        foreign_keys='[SolutionModel.user_id]',
        backref=db.backref(
            'user',
            lazy=True,
            uselist=False),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    accepts = db.relationship(
        'SolutionModel',
        primaryjoin='and_(SolutionModel.user_id==UserModel.id, SolutionModel.result==1)',
        foreign_keys='[SolutionModel.user_id]',
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self._statistics = UserStatisticsModel()

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = UserModel(
                username=forgery_py.internet.user_name(True),
                nickname=forgery_py.internet.user_name(True),
                email=forgery_py.internet.email_address(),
                password='123')
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @property
    def url(self):
        return url_for('profile.profile', user_id=self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    @hybrid_property
    def accepts_count(self):
        if self._statistics:
            return self._statistics.accepts_count
        else:
            return 0

    @accepts_count.setter
    def accepts_count_setter(self, value):
        if not self._statistics:
            self._statistics = UserStatisticsModel()
        self._statistics.accepts_count = value

    @accepts_count.expression
    def accepts_count_expr(cls):
        return UserStatisticsModel.accepts_count

    @property
    def ratio(self):
        return '%.f%%' % round(
            self.accepts_count * 100.0 / self.solutions_count
            if self.solutions_count else 0)

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def __repr__(self):
        return '<User %r>' % self.username


class UserFavoritesModel(db.Model):
    __tablename__ = 'user_favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False, index=True)
    problem_id = db.Column(db.Integer(), nullable=False, index=True)
    date_created = db.Column(
        db.DateTime(),
        server_default=db.func.current_timestamp(),
        nullable=False, index=True)


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
