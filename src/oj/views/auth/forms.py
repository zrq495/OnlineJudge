# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, SelectField,
    RadioField)
from wtforms.validators import (
    Required, Length, Email, Regexp, EqualTo, Optional)
from wtforms import ValidationError

from oj import app
from oj.models import UserModel
from oj.core.sensitive import censor


class LoginForm(Form):
    login_name = StringField(
        '邮箱或用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class SignupForm(Form):
    email = StringField(
        '邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、数字、点、下划线')])
    nickname = StringField('昵称', validators=[
        Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='两次密码不相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    gender = SelectField(
        '性别',
        choices=[
            ('male', '男'),
            ('female', '女')],
        validators=[Optional()])
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
    submit = SubmitField('注册')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')

    def validate_username(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('用户名中存在禁用词，请更换')
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_nickname(self, field):
        if censor.has_name_forbidden_word(field.data):
            raise ValidationError('昵称中存在禁用词，请更换')
        if UserModel.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在')


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
