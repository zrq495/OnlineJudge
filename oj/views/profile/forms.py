# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms.fields import (
    StringField, RadioField, SubmitField, SelectField)
from wtforms.validators import (
    Required, Optional, Length, Regexp, Email)
from wtforms import ValidationError
from flask.ext.login import current_user

from oj import app
from oj.models import UserModel
from oj.core.sensitive import censor


class UserForm(Form):

    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、数字、点、下划线')])
    nickname = StringField('昵称', validators=[
        Required(), Length(1, 64)])
    gender = RadioField(
        '性别', coerce=lambda x: x,
        choices=[
            ('male', '男'),
            ('female', '女')],
        validators=[
            Optional()])
    program_language = SelectField(
        '编程语言',
        choices=app.config['PROGRAM_LANGUAGE'].items(),
        validators=[Required()])
    school = StringField('学校')
    college = StringField('学院')
    major = StringField('专业')
    grade = StringField('年级')
    clazz = StringField('班级')
    qq = StringField('QQ')
    phone = StringField('手机号')
    address = StringField('地址')
    submit = SubmitField('修改')

    def validate_email(self, field):
        if current_user.email != field.data:
            if UserModel.query.filter_by(email=field.data).first():
                raise ValidationError('邮箱已经注册')

    def validate_username(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('用户名中存在禁用词，请更换')
        if current_user.username != field.data:
            if UserModel.query.filter_by(username=field.data).first():
                raise ValidationError('用户名已经存在')

    def validate_nickname(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('昵称中存在禁用词，请更换')
        if current_user.nickname != field.data:
            if UserModel.query.filter_by(nickname=field.data).first():
                raise ValidationError('昵称已经存在')
