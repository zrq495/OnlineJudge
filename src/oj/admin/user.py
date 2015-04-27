# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import xlrd
from sqlalchemy import or_
from collections import OrderedDict
from wtforms import fields
from flask import (
    current_app as app, views, render_template, request
)
from flask.ext.admin import expose, expose_plugview, BaseView
from flask.ext.login import current_user
from werkzeug.datastructures import MultiDict

from oj import db
from oj.models import UserModel, UserStatisticsModel
from .mixin import Mixin
from . import forms
from . import flask_admin


class UserAdmin(Mixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'id', 'username', 'nickname', 'email', 'date_created'
    ]
    column_searchable_list = ['username', 'nickname', 'email', 'school']
    column_filters = [
        'id', 'username', 'nickname', 'email', 'gender', 'school',
        'program_language', 'date_created'
    ]

    form_excluded_columns = [
        'password_hash', 'favorites', 'message_sent', 'message_received',
        'news', 'solutions', 'accepts', 'date_created', 'date_last_login',
        'last_login_ip', 'current_login_ip', 'date_current_login',
        'login_count', 'role_id', 'headlines'
    ]

    def __init__(self, session, **kwargs):
        super(UserAdmin, self).__init__(UserModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = fields.StringField('Password')
        return form_class

    def on_model_change(self, form, model):
        if len(model.password2):
            model.password = form.password2.data
        elif not model.password_hash:
            default_password = app.config['DEFAULT_PASSWORD']
            model.password = form.password2.data if len(model.password2) else default_password


class UserDeletedAdmin(Mixin):

    can_restore = True
    can_create = False
    can_edit = False
    can_delete = False

    column_list = [
        'id', 'username', 'nickname', 'email', 'date_deleted', 'reason'
    ]
    column_searchable_list = ['username', 'nickname', 'email', 'school']
    column_filters = [
        'id', 'username', 'nickname', 'email', 'gender', 'school',
        'program_language', 'date_deleted', 'reason'
    ]

    def __init__(self, session, **kwargs):
        super(UserDeletedAdmin, self).__init__(UserModel.deleted, session, **kwargs)


class UserStatisticsAdmin(Mixin):

    can_restore = False
    can_create = False
    can_edit = False
    can_delete = False

    def __init__(self, session, **kwargs):
        super(UserStatisticsAdmin, self).__init__(UserStatisticsModel, session, **kwargs)


class ImportUserView(BaseView):

    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

    @expose_plugview('/')
    class ImportUser(views.MethodView):
        template = 'admin/import_user.html'

        def get(self, cls):
            form = forms.ExcelUploadForm()
            return cls.render(self.template, form=form)

        def post(self, cls):
            values = MultiDict(request.form)
            if request.files:
                values.update(request.files)
            form = forms.ExcelUploadForm(values)
            if not form.validate():
                return self.error(cls, form)
            upload_file = form.upload_file.data
            book = xlrd.open_workbook(file_contents=upload_file.read())
            sheet = book.sheet_by_index(0)
            all_data = OrderedDict()
            for rownum in range(sheet.nrows):
                rowdata = sheet.row_values(rownum)
                all_data[rownum] = rowdata
            errors = OrderedDict()
            users = []
            for rownum, row in all_data.items():
                context = self.parse(row)
                if not context:
                    errors[rownum] = '数据格式不正确'
                    continue
                tmp_user = UserModel.query.filter(
                    or_(
                        UserModel.username == context['username'],
                        UserModel.nickname == context['nickname'],
                        UserModel.email == context['email'])).all()
                if tmp_user:
                    errors[rownum] = '用户已存在'
                    continue
                context['is_bulk_registration'] = True
                user = UserModel(**context)
                users.append(user)
            db.session.add_all(users)
            db.session.commit()
            return cls.render(
                self.template, form=form, errors=errors,
                users=users)

        def parse(self, row):
            context = {}
            try:
                context['username'] = row[0]
                context['nickname'] = row[1]
                context['email'] = row[2]
                context['password'] = row[3]
                context['gender'] = row[4]
                context['school'] = row[5]
                context['program_language'] = row[6]
            except Exception:
                return
            return context

        def error(self, cls, form):
            return cls.render(self.template, form=form)


flask_admin.add_view(UserAdmin(
    db.session, name='用户列表', category='用户管理', url='user'))
flask_admin.add_view(UserDeletedAdmin(
    db.session, name='垃圾用户列表', category='用户管理', url='user_deleted'))
flask_admin.add_view(UserStatisticsAdmin(
    db.session, name='用户统计', category='用户管理', url='user_statistics'))
flask_admin.add_view(ImportUserView(
    name='批量导入用户', category='用户管理', url='import_user'))
