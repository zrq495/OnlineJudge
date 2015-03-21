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
    contest_id = db.Column(db.Integer(), default=None)
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
