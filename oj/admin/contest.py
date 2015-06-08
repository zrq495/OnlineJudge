# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from wtforms import fields
from flask import current_app as app
from flask.ext.admin.model.form import InlineFormAdmin

from oj import db
from oj.models import ContestModel, ContestProblemModel
from .mixin import ModelViewMixin
from . import flask_admin
from .problem import CKTextAreaField


class ContestProblemModelInlineForm(InlineFormAdmin):

    form_excluded_columns = (
        'solutions', 'accepts', 'contest_id', 'problem_id', 'date_created')

    def __init__(self):
        return super(
            ContestProblemModelInlineForm, self).__init__(ContestProblemModel)


class ContestAdmin(ModelViewMixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = False

    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'

    column_list = [
        'id', 'name', 'user', 'date_start', 'date_end', 'status', 'type',
        'is_hidden', 'date_created']
    column_searchable_list = ['name']
    column_filters = [
        'id', 'name', 'is_hidden', 'date_created', 'date_start',
        'date_end', 'type']
    column_editable_list = ['is_hidden']

    form_excluded_columns = [
        'date_created', 'solutions', 'contest_users', 'user_id',
        'password_hash']
    form_overrides = dict(
        description=CKTextAreaField)

    inline_models = (ContestProblemModelInlineForm(),)

    def __init__(self, session, **kwargs):
        super(ContestAdmin, self).__init__(ContestModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(ContestAdmin, self).scaffold_form()
        form_class.password2 = fields.StringField('Password')
        return form_class

    def on_model_change(self, form, model):
        if len(model.password2):
            model.password = form.password2.data
        elif not model.password_hash:
            default_password = app.config['DEFAULT_PASSWORD']
            model.password = form.password2.data if len(model.password2) else default_password


flask_admin.add_view(ContestAdmin(
    db.session, name='比赛列表', category='比赛管理', url='contest'))
