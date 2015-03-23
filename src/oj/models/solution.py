# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db


__all__ = [
    'CodeModel',
    'SolutionModel',
    'CompileInfoModel',
]


class SolutionModel(db.Model):
    __tablename__ = 'solution'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    contest_id = db.Column(
        db.Integer(), nullable=False, default=0, server_default='0')
    problem_id = db.Column(db.Integer(), nullable=False)
    code_id = db.Column(db.Integer(), nullable=False)
    result = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    code = db.relationship(
        'CodeModel',
        primaryjoin='CodeModel.id==SolutionModel.code_id',
        foreign_keys='[SolutionModel.code_id]',
        backref=db.backref(
            'solution',
            uselist=False,
        )
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
        if contest_count == 0:
            ContestModel.generate_fake()
        if problem_count == 0:
            ProblemModel.generate_fake()
        for i in range(count):
            u = UserModel.query.offset(randint(0, user_count - 1)).first()
            c = ContestModel.query.offset(randint(0, contest_count - 1)).first()
            p = ProblemModel.query.offset(randint(0, problem_count - 1)).first()
            compile_info = CompileInfoModel(
                content=forgery_py.lorem_ipsum.paragraphs())
            db.session.add(compile_info)
            code = CodeModel(
                content=forgery_py.lorem_ipsum.paragraphs(),
                length=randint(1, 0xffff),
                take_time=randint(1, 0xffff),
                take_memory=randint(1, 0xffff),
                program_language=randint(0, 7),
                compile_info=compile_info)
            db.session.add(code)
            s = SolutionModel(
                user_id=u.id,
                contest_id=choice([0, c.id]),
                problem_id=p.id,
                code=code,
                result=randint(0, 3))
            db.session.add(s)
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
    content = db.Column(db.UnicodeText(), nullable=False)
    length = db.Column(db.Integer(), nullable=False)
    take_time = db.Column(db.Integer(), nullable=False)
    take_memory = db.Column(db.Integer(), nullable=False)
    program_language = db.Column(db.String(64), nullable=False)
    compile_info_id = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    compile_info = db.relationship(
        'CompileInfoModel',
        primaryjoin='CompileInfoModel.id==CodeModel.compile_info_id',
        foreign_keys='[CodeModel.compile_info_id]',
        backref=db.backref(
            'code',
            uselist=False,
        )
    )

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<Code %r>' % self.id


class CompileInfoModel(db.Model):
    __tablename__ = 'compile_info'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.UnicodeText(), default=None)
    date_created = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
        }

    def __repr__(self):
        return '<CompileInfo %r>' % self.id
