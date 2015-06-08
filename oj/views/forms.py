# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import fields, validators, ValidationError

from oj import app
from oj.models import ContestProblemModel


class ProblemSearchForm(Form):
    problem_id = fields.IntegerField(
        'Problem ID', validators=[validators.Optional()])
    problem_title = fields.StringField(
        'Problem Title', validators=[validators.Optional()])
    submit = fields.SubmitField('Search')


class SolutionSearchForm(Form):
    solution_id = fields.IntegerField(
        'Run ID', validators=[validators.Optional()])
    problem_id = fields.IntegerField(
        'Problem ID', validators=[validators.Optional()])
    contest_id = fields.IntegerField(
        'Contest ID', validators=[validators.Optional()])
    username = fields.StringField(
        'Username', validators=[validators.Optional()])
    language = fields.SelectField(
        'Language',
        coerce=lambda s: s if s else None,
        choices=[('', 'all')] + app.config['PROGRAM_LANGUAGE'].items(),
        validators=[validators.Optional()])
    result = fields.SelectField(
        'Result',
        coerce=lambda s: s if s == '' else None,
        choices=[('', 'all')] + app.config['SOLUTION_RESULT'].items(),
        validators=[validators.Optional()])
    submit = fields.SubmitField('Search')


class SubmitForm(Form):
    problem_id = fields.IntegerField(
        'Problem ID', validators=[validators.Required()])
    language = fields.SelectField(
        'Language',
        choices=app.config['PROGRAM_LANGUAGE'].items(),
        validators=[validators.Required()])
    code = fields.TextAreaField(
        'Source Code',
        validators=[validators.Optional(), validators.Length(3, 100000)])
    submit = fields.SubmitField('Submit')

    def validate_problem_id(self, field):
        # TODO 验证题目状态
        pass


class ContestSubmitForm(Form):
    contest_problem_id = fields.IntegerField(
        'Contest_Problem ID', validators=[validators.Required()])
    language = fields.SelectField(
        'Language',
        choices=app.config['PROGRAM_LANGUAGE'].items(),
        validators=[validators.Required()])
    code = fields.TextAreaField(
        'Source Code',
        validators=[validators.Optional(), validators.Length(3, 100000)])
    submit = fields.SubmitField('Submit')

    def validate_contest_problem_id(self, field):
        contest_problem_id = field.data
        contest_problem = ContestProblemModel.query.get(
            contest_problem_id)
        if not contest_problem:
            raise ValidationError('题目不存在')
        if contest_problem.contest.is_hidden:
            raise ValidationError('比赛不存在')
        if contest_problem.contest.status == 'pending':
            raise ValidationError('比赛还没开始')
        if contest_problem.contest.status == 'ended':
            raise ValidationError('比赛已经结束')
