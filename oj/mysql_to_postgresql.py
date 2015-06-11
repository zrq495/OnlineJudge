# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import random
import string
import MySQLdb
import MySQLdb.cursors
import psycopg2
import psycopg2.extras
from flask.ext.wtf import Form
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, SelectField,
    RadioField, DateTimeField)
from wtforms.validators import (
    Required, Length, Email, Regexp, EqualTo, Optional)

from oj import db, app
from oj.models import *

m_con = MySQLdb.connect(
    host="210.44.176.195", port=3306, user="root", passwd="OcnuRW_B+>",
    db="oj", cursorclass=MySQLdb.cursors.DictCursor, charset='utf8')
m_cur = m_con.cursor()

p_con = psycopg2.connect(
    host='localhost', dbname='oj', user='oj', password='oooo')
# p_cur = p_con.cursor()
p_cur = p_con.cursor(cursor_factory=psycopg2.extras.DictCursor)

# m_users = m_cur.execute('select user_id, user_name, nick_name, email, school, reg_time, pro_lang, last_ip, last_time, qq, tel, addr, sex, college, major, grade, class, batch_registration from user')
# p_cur.executemany('insert into "user" (id, username, nick_name, email, school, date_created, program_language, last_login_ip, date_last_login, qq, phone, address, gender, ) values ()')


default_password = app.config['DEFAULT_PASSWORD']
program_language = app.config['PROGRAM_LANGUAGE']


def get_random_email():
    email = ''
    n = random.randint(6, 10)
    for i in xrange(n):
        email += random.choice(string.letters)
    email += '@'
    for i in xrange(n / 2):
        email += random.choice(string.letters)
    email += '.'
    for i in xrange(n / 2):
        email += random.choice(string.letters)
    user = UserModel.query.filter(UserModel.email == email).first()
    if user:
        return get_random_email()
    return email


def get_random_username():
    username = ''
    n = random.randint(10, 15)
    for i in xrange(n):
        username += random.choice(string.letters)
    user = UserModel.query.filter(UserModel.username == username).first()
    if user:
        return get_random_username()
    return username


def get_random_nickname():
    nickname = ''
    n = random.randint(10, 15)
    for i in xrange(n):
        nickname += random.choice(string.letters)
    user = UserModel.query.filter(UserModel.nickname == nickname).first()
    if user:
        return get_random_nickname()
    return nickname


class UserForm(Form):
    email = StringField(
        '邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、数字、点、下划线')])
    nickname = StringField('昵称', validators=[
        Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[
        Required()])
    gender = SelectField(
        '性别',
        choices=[
            ('male', '男'),
            ('female', '女')],
        validators=[Optional()])
    program_language = SelectField(
        '编程语言',
        choices=program_language.items(),
        validators=[Required()])
    school = StringField('学校')
    college = StringField('学院')
    major = StringField('专业')
    grade = StringField('年级')
    clazz = StringField('班级')
    qq = StringField('QQ')
    phone = StringField('手机号')
    address = StringField('地址')
    is_bulk_registration = BooleanField()
    last_login_ip = StringField()
    date_last_login = DateTimeField()
    date_created = DateTimeField()

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            field.data = get_random_email()

    def validate_username(self, field):
        if UserModel.query.filter_by(username=field.data).first():
            field.data += get_random_username()

    def validate_nickname(self, field):
        if UserModel.query.filter_by(nickname=field.data).first():
            field.data += get_random_nickname()

user_map = {
    'user_id': 'id',
    'nick_name': 'nickname',
    'user_name': 'username',
    'pro_lang': 'program_language',
    'sex': 'gender',
    'class': 'clazz',
    'tel': 'phone',
    'addr': 'address',
    'last_ip': 'last_login_ip',
    'last_time': 'date_last_login',
    'reg_time': 'date_created',
    'batch_registration': 'is_bulk_registration',
}


def validate_user(user):
    map(lambda x: user.update({user_map[x]: user[x]}), user_map)
    user['password'] = default_password
    if user['gender'] in ['女', 'female', 'f', 'F']:
        user['gender'] = 'female'
    else:
        user['gender'] = 'male'
    if not user['date_last_login']:
        user['date_last_login'] = datetime.datetime.now()
    if not user['email']:
        user['email'] = get_random_email()
    if not user['username']:
        user['username'] = get_random_username()
    if not user['nickname']:
        user['nickname'] = get_random_nickname()
    if not user['is_bulk_registration']:
        user['is_bulk_registration'] = False
    if not user['program_language'] or user['program_language'].lower() not in program_language.keys():
        user['program_language'] = 'gcc'
    user['program_language'] = user['program_language'].lower()


def import_user():
    m_cur.execute('select * from user')
    m_users = m_cur.fetchall()
    for m_user in m_users:
        # if m_user['user_id'] < 17160:
            # continue
        validate_user(m_user)
        form = UserForm(csrf_enabled=False, **m_user)
        form.validate()
        user = UserModel.query.get(m_user['id'])
        if not user:
            user = UserModel()
            db.session.add(user)
        user.id = m_user['id']
        form.populate_obj(user)
        db.session.commit()
        print user.id, m_user['id']
