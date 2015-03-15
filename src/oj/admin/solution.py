# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask.ext.admin.contrib.sqla import ModelView

from oj import flask_admin, db
from oj.models import SolutionModel

flask_admin.add_view(ModelView(SolutionModel, db.session))
