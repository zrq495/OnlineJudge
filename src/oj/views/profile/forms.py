# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms.fields import (
    StringField, RadioField, SubmitField)
from wtforms.validators import (
    Required, Optional, Length, Regexp, Email)
from wtforms import ValidationError
from flask.ext.login import current_user

from oj.models import UserModel


class UserForm(Form):

    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    nickname = StringField('Nickname', validators=[
        Required(), Length(1, 64)])
    gender = RadioField(
        'gender', coerce=lambda x: x,
        choices=[
            ('male', 'male'),
            ('female', 'female')],
        validators=[
            Optional()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if current_user.email != field.data:
            if UserModel.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if current_user.username != field.data:
            if UserModel.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use.')

    def validate_nickname(self, field):
        if current_user.nickname != field.data:
            if UserModel.query.filter_by(nickname=field.data).first():
                raise ValidationError('Nickname already in use.')
