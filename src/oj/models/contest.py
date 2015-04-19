# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import sql
from flask import url_for

from oj import db
from .user import UserModel


__all__ = [
    'ContestModel',
    'ContestProblemModel',
    'ContestUserModel',
]


class ContestModel(db.Model):
    __tablename__ = 'contest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(512), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.UnicodeText)
    type = db.Column(
        db.Enum('public', 'private', 'register', 'diy',
                name='contest_type_enum'),
        server_default='public', nullable=False)
    user_id = db.Column(db.Integer(), nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    date_start_register = db.Column(db.DateTime)
    date_end_register = db.Column(db.DateTime)
    is_hiden = db.Column(
        db.Boolean, default=False, server_default=sql.false(),
        nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    user = db.relationship(
        'UserModel',
        primaryjoin='UserModel.id==ContestModel.user_id',
        foreign_keys='[ContestModel.user_id]',
        lazy=True
    )

    contest_users = db.relationship(
        'ContestUserModel',
        primaryjoin='and_(ContestUserModel.contest_id==ContestModel.id, ContestModel.type=="register")',
        foreign_keys='[ContestUserModel.contest_id]',
        backref=db.backref(
            'contest',
            lazy=True),
        passive_deletes='all',
        lazy='dynamic'
    )

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='SolutionModel.contest_id==ContestModel.id',
        foreign_keys='[SolutionModel.contest_id]',
        backref=db.backref(
            'contest',
            lazy=True,
            uselist=False),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    problems = db.relationship(
        'ContestProblemModel',
        primaryjoin='ContestProblemModel.contest_id==ContestModel.id',
        foreign_keys='[ContestProblemModel.contest_id]',
        backref=db.backref(
            'contest',
            lazy=True),
        order_by='ContestProblemModel.ordinal.asc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint, choice
        import forgery_py

        seed()
        now = datetime.datetime.now()
        user_count = UserModel.query.count()
        if user_count == 0:
            UserModel.generate_fake()
            user_count = UserModel.query.count()
        for i in range(count):
            date_start = now + datetime.timedelta(randint(-100, 100))
            date_end = date_start + datetime.timedelta(hours=randint(2, 10))
            date_end_register = date_start - datetime.timedelta(randint(1,5))
            date_start_register = date_end_register - datetime.timedelta(randint(1,10))
            u = UserModel.query.offset(randint(0, user_count - 1)).first()
            c = ContestModel(
                name=forgery_py.lorem_ipsum.title(),
                date_start=date_start,
                date_end=date_end,
                description=forgery_py.lorem_ipsum.paragraph(),
                type=choice(['public', 'private', 'register', 'diy']),
                user_id=u.id,
                password='123',
                date_start_register=date_start_register,
                date_end_register=date_end_register,
            )
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @property
    def url(self):
        return url_for('contest.detail', contest_id=self.id)

    @property
    def status(self):
        now = datetime.datetime.now()
        if now < self.date_start:
            status = 'pending'
        elif now > self.date_end:
            status = 'ended'
        else:
            status = 'running'
        return status

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return '<Contest %r>' % self.name


class ContestProblemModel(db.Model):
    __tablename__ = 'contest_problem'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(512))
    contest_id = db.Column(db.Integer(), nullable=False, index=True)
    problem_id = db.Column(db.Integer(), nullable=False, index=True)
    ordinal = db.Column(db.Integer(), default=0, server_default='0', index=True)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    problem = db.relationship(
        'ProblemModel',
        primaryjoin='ProblemModel.id==ContestProblemModel.problem_id',
        foreign_keys='[ContestProblemModel.problem_id]',
        lazy=True
    )

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='and_(SolutionModel.problem_id==ContestProblemModel.problem_id, SolutionModel.contest_id==ContestProblemModel.contest_id)',
        foreign_keys='[SolutionModel.problem_id, SolutionModel.contest_id]',
        backref=db.backref(
            'contest_problem',
            lazy=True
        ),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    accepts = db.relationship(
        'SolutionModel',
        primaryjoin='and_(SolutionModel.problem_id==ContestProblemModel.problem_id, SolutionModel.contest_id==ContestProblemModel.contest_id, SolutionModel.result==1)',
        foreign_keys='[SolutionModel.problem_id, SolutionModel.contest_id]',
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        from .problem import ProblemModel

        seed()
        contest_count = ContestModel.query.count()
        problem_count = ProblemModel.query.count()
        if contest_count == 0:
            ContestModel.generate_fake()
            contest_count = ContestModel.query.count()
        if problem_count == 0:
            ProblemModel.generate_fake()
            problem_count = ProblemModel.query.count()
        for i in range(count):
            c = ContestModel.query.offset(randint(0, contest_count - 1)).first()
            p = ProblemModel.query.offset(randint(0, problem_count - 1)).first()
            cp = ContestProblemModel(
                name=p.title,
                contest_id=c.id,
                problem_id=p.id,
                ordinal=randint(0, 0xffff))
            db.session.add(cp)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<ContestProblem %r>' % self.id


class ContestUserModel(db.Model):
    __tablename__ = 'contest_user'

    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer(), nullable=False, index=True)
    team_name = db.Column(db.Unicode(256), nullable=False)
    status = db.Column(
        db.Enum(
            'accept', 'waiting', 'reject', 'again',
            name='contest_user_status_enum'),
        server_default='waiting', nullable=False, index=True)
    seat_number = db.Column(db.Unicode(128))
    reason = db.Column(db.Unicode(256))
    user_id = db.Column(db.Integer(), nullable=False, index=True)

    student_id = db.Column(db.String(32))
    name = db.Column(db.Unicode(256))
    school = db.Column(db.Unicode(256))
    college = db.Column(db.Unicode(256))
    major = db.Column(db.Unicode(256))
    clazz = db.Column(db.Unicode(256))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(256))
    student_id1 = db.Column(db.String(32))
    name1 = db.Column(db.Unicode(256))
    school1 = db.Column(db.Unicode(256))
    college1 = db.Column(db.Unicode(256))
    major1 = db.Column(db.Unicode(256))
    clazz1 = db.Column(db.Unicode(256))
    phone1 = db.Column(db.String(32))
    email1 = db.Column(db.String(256))
    student_id2 = db.Column(db.String(32))
    name2 = db.Column(db.Unicode(256))
    school2 = db.Column(db.Unicode(256))
    college2 = db.Column(db.Unicode(256))
    major2 = db.Column(db.Unicode(256))
    clazz2 = db.Column(db.Unicode(256))
    phone2 = db.Column(db.String(32))
    email2 = db.Column(db.String(256))
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='and_(SolutionModel.user_id==ContestUserModel.user_id, SolutionModel.contest_id==ContestUserModel.contest_id)',
        foreign_keys='[SolutionModel.user_id, SolutionModel.contest_id]',
        backref=db.backref(
            'contest_user',
            lazy=True
        ),
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    accepts = db.relationship(
        'SolutionModel',
        primaryjoin='and_(SolutionModel.user_id==ContestUserModel.user_id, SolutionModel.contest_id==ContestUserModel.contest_id, SolutionModel.result==1)',
        foreign_keys='[SolutionModel.user_id, SolutionModel.contest_id]',
        order_by='SolutionModel.date_created.desc()',
        passive_deletes='all',
        lazy='dynamic'
    )

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<ContestUser %r>' % self.id
