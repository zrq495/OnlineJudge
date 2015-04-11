# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from wtforms import fields
from flask import current_app as app

from oj import flask_admin, db
from oj.models import UserModel, UserStatisticsModel
from .mixin import Mixin


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
        'news', 'solutions', 'accepts', 'date_created'
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


flask_admin.add_view(UserAdmin(
    db.session, name='用户列表', category='用户管理', url='user'))
flask_admin.add_view(UserDeletedAdmin(
    db.session, name='垃圾用户列表', category='用户管理', url='user_deleted'))
flask_admin.add_view(UserStatisticsAdmin(
    db.session, name='用户统计', category='用户管理', url='user_statistics'))
