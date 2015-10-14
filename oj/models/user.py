# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sqlalchemy import sql
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin, AnonymousUserMixin

from oj import db, login_manager
from .role import Permission

from hashlib import md5


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
    college = db.Column(db.String(256))
    major = db.Column(db.String(256))
    grade = db.Column(db.String(64))
    clazz = db.Column(db.String(64))
    program_language = db.Column(
        db.Enum('gcc', 'g++', 'java', name='user_program_language_enum'))
    avatar = db.Column(db.String(256))
    qq = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    address = db.Column(db.String(256))
    role_id = db.Column(db.Integer)
    is_bulk_registration = db.Column(
        db.Boolean, default=False, server_default=sql.false(), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    last_login_ip = db.Column(db.String(64))
    current_login_ip = db.Column(db.String(64))
    login_count = db.Column(db.Integer())
    date_last_login = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())
    date_current_login = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())
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

    headlines = db.relationship(
        'HeadlineModel',
        primaryjoin='HeadlineModel.user_id==UserModel.id',
        foreign_keys='[HeadlineModel.user_id]',
        backref=db.backref(
            'user',
            lazy=True,
            uselist=False),
        order_by='HeadlineModel.date_created.desc()',
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

    role = db.relationship(
        'RoleModel',
        primaryjoin='UserModel.role_id==RoleModel.id',
        foreign_keys='[UserModel.role_id]',
        backref=db.backref(
            'user',
            lazy='dynamic'),
        lazy=True)

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self._statistics = UserStatisticsModel()

    @property
    def email_md5(self):
        email = self.email.strip()
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        return md5(email).hexdigest()

    def g_avatar(self, size=48, default='retro', rating='g'):
        return "{url}{hash}?d={default}&s={size}".format(
            url=current_app.config['GRAVATAR_BASE_URL'],
            hash=self.email_md5,
            default=default,
            size=size,
            rating=rating
        )

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

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

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

    def can(self, permissions):
        return (self.role is not None and
                (self.role.permissions & permissions) == permissions)

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

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


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
