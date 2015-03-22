# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask.ext.admin.contrib.sqla import ModelView

from oj import flask_admin, db
from oj.models import ProblemModel


class ProblemModelView(ModelView):
    # Disable model creation
    # can_create = False

    # Override displayed fields
    # column_list = ('title',)

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProblemModelView, self).__init__(ProblemModel, session, **kwargs)


flask_admin.add_view(ProblemModelView(db.session))
