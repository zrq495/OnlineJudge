# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db
from oj.models import CodeModel, CompileInfoModel
from .mixin import Mixin
from . import flask_admin

flask_admin.add_view(Mixin(CodeModel, db.session))
flask_admin.add_view(Mixin(CompileInfoModel, db.session))
