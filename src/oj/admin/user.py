# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from wtforms import fields

from oj import flask_admin, db
from oj.models import UserModel
from .mixin import Mixin


class User(Mixin):

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
        super(User, self).__init__(UserModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(User, self).scaffold_form()
        form_class.password2 = fields.PasswordField('Password')
        return form_class

    def on_model_change(self, form, model):
        if len(model.password2):
            model.password = form.password2.data


class UserDeleted(Mixin):

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
        super(UserDeleted, self).__init__(UserModel.deleted, session, **kwargs)


flask_admin.add_view(User(
    db.session, name='用户列表', category='用户管理', endpoint='user'))
flask_admin.add_view(UserDeleted(
    db.session, name='垃圾用户列表', category='用户管理', endpoint='user_deleted'))
