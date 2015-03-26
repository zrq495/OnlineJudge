# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import fields, validators, ValidationError


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
    username = fields.StringField(
        'Username', validators=[validators.Optional()])
    language = fields.SelectField(
        'Language',
        coerce=lambda s: s if s else None,
        choices=[('', 'all'), ('gcc', 'gcc'), ('python', 'Python')],
        validators=[validators.Optional()])
    result = fields.SelectField(
        'Result',
        coerce=lambda s: s if s else None,
        choices=[('', 'all'), ('0', '0'), ('1', '1')],
        validators=[validators.Optional()])
    submit = fields.SubmitField('Search')
