# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import sql

from oj import db


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
    user_id = db.Column(db.Integer(), nullable=False)
    password_hash = db.Column(db.String(128))
    date_start_register = db.Column(db.DateTime, nullable=False)
    date_end_register = db.Column(db.DateTime, nullable=False)
    is_hiden = db.Column(
        db.Boolean, default=False, server_default=sql.false(),
        nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    user = db.relationship(
        'UserModel',
        primaryjoin='UserModel.id==ContestModel.user_id',
        foreign_keys='[ContestModel.user_id]',
        lazy=True
    )

    solutions = db.relationship(
        'SolutionModel',
        primaryjoin='SolutionModel.contest_id==ContestModel.id',
        foreign_keys='[SolutionModel.contest_id]',
        backref=db.backref(
            'contest',
            lazy=True,
            uselist=False,
            innerjoin=True),
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
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            c = ContestModel(
                name=forgery_py.lorem_ipsum.name())
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

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
    contest_id = db.Column(db.Integer(), nullable=False)
    problem_id = db.Column(db.Integer(), nullable=False)
    ordinal = db.Column(db.Integer(), default=0, server_default='0')
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    problem = db.relationship(
        'ProblemModel',
        primaryjoin='ProblemModel.id==ContestProblemModel.problem_id',
        foreign_keys='[ContestProblemModel.problem_id]',
        lazy=True
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
    contest_id = db.Column(db.Integer(), nullable=False)
    login_name = db.Column(db.String(256), nullable=False)
    team_name = db.Column(db.Unicode(256), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    status = db.Column(
        db.Enum(
            'accept', 'waiting', 'reject', 'again',
            name='contest_user_status_enum'),
        server_default='waiting', nullable=False)
    seat_number = db.Column(db.Unicode(128))
    reason = db.Column(db.Unicode(256))
    user_id = db.Column(db.Integer(), nullable=False)
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
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

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
        }

    def __repr__(self):
        return '<ContestUser %r>' % self.id
