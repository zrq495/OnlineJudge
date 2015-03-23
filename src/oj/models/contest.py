# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'ContestModel',
    'ContestProblemModel',
    'ContestUserModel',
]


class ContestModel(db.Model):
    __tablename__ = 'contest'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

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
            lazy='joined',
            innerjoin=True),
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
                title=forgery_py.lorem_ipsum.title())
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def __repr__(self):
        return '<Contest %r>' % self.title


class ContestProblemModel(db.Model):
    __tablename__ = 'contest_problem'

    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer(), nullable=False)
    problem_id = db.Column(db.Integer(), nullable=False)
    ordinal = db.Column(db.Integer(), default=0)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    problem = db.relationship(
        'ProblemModel',
        primaryjoin='ProblemModel.id==ContestProblemModel.problem_id',
        foreign_keys='[ContestProblemModel.problem_id]',
        uselist=False
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
        if problem_count == 0:
            ProblemModel.generate_fake()
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
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<ContestUser %r>' % self.id
