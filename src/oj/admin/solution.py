# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db
from oj.models import SolutionModel, CodeModel, CompileInfoModel
from .mixin import Mixin
from . import flask_admin


class SolutionAdmin(Mixin):

    can_restore = False
    can_create = False
    can_edit = False
    can_delete = False

    def __init__(self, session, **kwargs):
        super(SolutionAdmin, self).__init__(SolutionModel, session, **kwargs)


class CodeAdmin(Mixin):

    can_restore = False
    can_create = False
    can_edit = True
    can_delete = False

    column_list = ['id', 'solution_id', 'date_created', 'solution', 'linage']

    form_excluded_columns = ['date_created', 'solution', 'compile_info']

    def __init__(self, session, **kwargs):
        super(CodeAdmin, self).__init__(CodeModel, session, **kwargs)


class CompileInfoAdmin(Mixin):

    can_restore = False
    can_create = False
    can_edit = True
    can_delete = False

    def __init__(self, session, **kwargs):
        super(CompileInfoAdmin, self).__init__(CompileInfoModel, session, **kwargs)


flask_admin.add_view(SolutionAdmin(
    db.session, name='提交纪录', category='提交管理', url='solution'))
flask_admin.add_view(CodeAdmin(
    db.session, name='代码列表', category='提交管理', url='code'))
flask_admin.add_view(CompileInfoAdmin(
    db.session, name='编译信息', category='提交管理', url='compile'))
