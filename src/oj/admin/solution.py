# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db
from oj.models import SolutionModel
from .mixin import Mixin
from . import flask_admin

flask_admin.add_view(Mixin(SolutionModel, db.session))
