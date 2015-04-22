# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from wtforms import fields, widgets

from oj import db
from oj.models import ProblemModel, ProblemStatisticsModel
from .mixin import Mixin
from . import flask_admin


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class ProblemAdmin(Mixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = False

    create_template = 'admin/edit_problem.html'
    edit_template = 'admin/edit_problem.html'

    column_list = [
        'id', 'title', 'source', 'is_display', 'date_created'
    ]
    column_searchable_list = ['title', 'source', 'author']
    column_filters = [
        'id', 'title', 'source', 'is_display', 'date_created', 'date_modified'
    ]

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


class ProblemStatisticsAdmin(Mixin):

    can_restore = False
    can_create = False
    can_edit = False
    can_delete = False

    def __init__(self, session, **kwargs):
        super(ProblemStatisticsAdmin, self).__init__(ProblemStatisticsModel, session, **kwargs)


flask_admin.add_view(ProblemAdmin(
    db.session, name='题目列表', category='题目管理', url='problem'))
flask_admin.add_view(ProblemStatisticsAdmin(
    db.session, name='题目统计', category='题目管理', url='problem_statistics'))
