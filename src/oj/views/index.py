# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   Blueprint,
                   render_template)
from flask.ext.login import current_user

from oj.models import UserModel


class IndexView(views.MethodView):

    def get(self):
        user = current_user
        return render_template(
            'index.html',
            user=user)


bp_index = Blueprint('index', __name__)
bp_index.add_url_rule(
    '',
    view_func=IndexView.as_view(b'index'),
    methods=['GET'])
