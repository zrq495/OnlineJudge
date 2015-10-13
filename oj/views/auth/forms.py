# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import (
    Required, Length, Email, Regexp, EqualTo)
from wtforms import ValidationError

from oj.models import UserModel
from oj.core.sensitive import censor


class LoginForm(Form):
    login_name = StringField(
        'Email or Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class SignupForm(Form):
    email = StringField(
        'Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Username must have only letters,'
                                          'numbers, dots or underscores')])
    nickname = StringField('Nickname', validators=[
        Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email has already been registered')

    def validate_username(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('Username exists disabled word, '
                                  'please change')
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

    def validate_nickname(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('Nickname exists disabled word, '
                                  'please change')
        if UserModel.query.filter_by(nickname=field.data).first():
            raise ValidationError('Nickname already in use')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次密码不相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('修改密码')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[
        Required(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱不存在')


class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='两次密码不相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱不存在')
