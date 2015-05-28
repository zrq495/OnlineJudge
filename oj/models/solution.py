# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import url_for

from oj import db


__all__ = [
    'CodeModel',
    'SolutionModel',
    'CompileInfoModel',
]


class SolutionModel(db.Model):
    __tablename__ = 'solution'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), index=True)
    contest_id = db.Column(
        db.Integer(), nullable=False, default=0,
        server_default='0', index=True)
    problem_id = db.Column(db.Integer(), nullable=False, index=True)
    result = db.Column(
        db.Integer(), nullable=False, index=True,
        default=0, server_default='0')
    length = db.Column(
        db.Integer(), nullable=False, default=0, server_default='0')
    take_time = db.Column(
        db.Integer(), nullable=False, default=0, server_default='0')
    take_memory = db.Column(
        db.Integer(), nullable=False, default=0, server_default='0')
    program_language = db.Column(
        db.Enum('gcc', 'g++', 'java', name='solution_program_language_enum'),
        nullable=False, index=True)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    code = db.relationship(
        'CodeModel',
        primaryjoin='CodeModel.solution_id==SolutionModel.id',
        foreign_keys='[CodeModel.solution_id]',
        backref='solution',
        uselist=False
    )

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint, choice
        import forgery_py

        from .user import UserModel
        from .contest import ContestModel
        from .problem import ProblemModel

        seed()
        user_count = UserModel.query.count()
        contest_count = ContestModel.query.count()
        problem_count = ProblemModel.query.count()
        if user_count == 0:
            UserModel.generate_fake()
            user_count = UserModel.query.count()
        if contest_count == 0:
            ContestModel.generate_fake()
            contest_count = ContestModel.query.count()
        if problem_count == 0:
            ProblemModel.generate_fake()
            problem_count = ProblemModel.query.count()
        for i in range(count):
            u = UserModel.query.offset(randint(0, user_count - 1)).first()
            c = ContestModel.query.offset(randint(0, contest_count - 1)).first()
            p = ProblemModel.query.offset(randint(0, problem_count - 1)).first()
            # TODO add contest problem solution to contest
            s = SolutionModel(
                user_id=u.id,
                contest_id=choice([0, c.id]),
                problem_id=p.id,
                result=randint(0, 3),
                length=randint(1, 0xfff),
                take_time=randint(1, 0xffff),
                take_memory=randint(1, 0xffff),
                program_language=choice(['gcc', 'g++', 'java']))
            db.session.add(s)
            code = CodeModel(
                content=forgery_py.lorem_ipsum.paragraphs(),
                solution=s)
            db.session.add(code)
            compile_info = CompileInfoModel(
                content=forgery_py.lorem_ipsum.paragraphs(),
                code=code)
            db.session.add(compile_info)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<Solution %r>' % self.id


class CodeModel(db.Model):
    __tablename__ = 'code'

    id = db.Column(db.Integer, primary_key=True)
    solution_id = db.Column(db.Integer(), nullable=False, index=True)
    content = db.Column(db.UnicodeText(), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    compile_info = db.relationship(
        'CompileInfoModel',
        primaryjoin='CompileInfoModel.code_id==CodeModel.id',
        foreign_keys='[CompileInfoModel.code_id]',
        backref='code',
        uselist=False
    )

    @property
    def linage(self):
        return len(self.content.splitlines())

    @property
    def url(self):
        return url_for('code.detail', code_id=self.id)

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<Code %r>' % self.id


class CompileInfoModel(db.Model):
    __tablename__ = 'compile_info'

    id = db.Column(db.Integer, primary_key=True)
    code_id = db.Column(db.Integer(), nullable=False, index=True)
    content = db.Column(db.UnicodeText(), default=None)
    date_created = db.Column(
        db.DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<CompileInfo %r>' % self.id
