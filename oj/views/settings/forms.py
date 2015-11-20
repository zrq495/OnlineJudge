# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms.fields import (
    StringField, RadioField, SubmitField, SelectField, PasswordField)
from wtforms.validators import (
    Required, Optional, Length, Email)
from wtforms import ValidationError
from flask.ext.login import current_user

from oj import app
from oj.models import UserModel
from oj.core.sensitive import censor


class ProfileForm(Form):

    nickname = StringField('Nickname', validators=[
        Required(), Length(1, 64)])
    gender = RadioField(
        'Gender', coerce=lambda x: x,
        choices=[
            ('male', 'Male'),
            ('female', 'Female')],
        validators=[
            Optional()])
    program_language = SelectField(
        'Program Language',
        choices=app.config['PROGRAM_LANGUAGE'].items(),
        validators=[Required()])
    school = StringField('School')
    college = StringField('College')
    major = StringField('Major')
    grade = StringField('Grade')
    clazz = StringField('Class')
    qq = StringField('QQ')
    phone = StringField('Phone')
    address = StringField('Address')
    submit = SubmitField('Update profile')

    def validate_nickname(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('Nickname exists disabled word, '
                                  'please change')
        if current_user.nickname != field.data:
            if UserModel.query.filter_by(nickname=field.data).first():
                raise ValidationError('Nickname already in use')


class ChangeEmailForm(Form):
    new_email = StringField('New Email', validators=[Required(), Email()])
    password = PasswordField('Verify Password', validators=[Required()])
    submit = SubmitField('Change Email')

    def validate_new_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email has already been registered')

    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Invalid password.')
