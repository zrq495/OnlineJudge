# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from wtforms import fields, widgets
from flask.ext.login import current_user
from flask.ext.admin.contrib import fileadmin

from oj import db, app
from oj.models import ProblemModel, ProblemStatisticsModel
from .mixin import ModelViewMixin
from . import flask_admin


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs['class'] = (
            kwargs.setdefault('class', '') + ' ckeditor').strip()
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class ProblemAdmin(ModelViewMixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = False

    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'

    column_list = [
        'id', 'title', 'source', 'is_display', 'date_created'
    ]
    column_searchable_list = ['title', 'source', 'author']
    column_filters = [
        'id', 'title', 'source', 'is_display', 'date_created', 'date_modified'
    ]
    column_editable_list = ['is_display']

    form_overrides = dict(
        description=CKTextAreaField,
        input=CKTextAreaField,
        output=CKTextAreaField,
        sample_input=CKTextAreaField,
        sample_output=CKTextAreaField,
        hint=CKTextAreaField,
        source=CKTextAreaField,
        sample_code=CKTextAreaField,
    )
    form_excluded_columns = [
        'solution_users', 'accept_users', 'solutions',
        'accepts', 'date_created', 'date_modified'
    ]

    def __init__(self, session, **kwargs):
        super(ProblemAdmin, self).__init__(ProblemModel, session, **kwargs)


class ProblemStatisticsAdmin(ModelViewMixin):

    can_restore = False
    can_create = False
    can_edit = False
    can_delete = False

    def __init__(self, session, **kwargs):
        super(ProblemStatisticsAdmin, self).__init__(ProblemStatisticsModel, session, **kwargs)


class ProblemTestDataAdmin(fileadmin.FileAdmin):

    # TODO 多文件上传

    allowed_extensions = ('in', 'out')
    editable_extensions = ('in', 'out')

    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())


flask_admin.add_view(ProblemAdmin(
    db.session, name='题目列表', category='题目管理', url='problem'))
flask_admin.add_view(ProblemStatisticsAdmin(
    db.session, name='题目统计', category='题目管理', url='problem_statistics'))
flask_admin.add_view(
    ProblemTestDataAdmin(
        app.config['TEST_DATA_PATH'], category='题目管理', name='测试数据管理',
        url='problem_test_data'))
