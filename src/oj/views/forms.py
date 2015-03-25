# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import fields, validators, ValidationError


class ProblemSearchForm(Form):
    problem_id = fields.IntegerField(
        'problem_id', validators=[validators.Optional()])
    problem_title = fields.StringField(
        'problem_title', validators=[validators.Optional()])
    submit = fields.SubmitField('Search')
