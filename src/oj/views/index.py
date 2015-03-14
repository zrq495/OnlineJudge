# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   Blueprint,
                   render_template)

from oj.models import UserModel


class IndexView(views.MethodView):

    def get(self):
        user = UserModel.query.first()
        return render_template(
            'index.html',
            name=user.username if user else None)


bp_index = Blueprint('index', __name__)
bp_index.add_url_rule(
    '',
    view_func=IndexView.as_view(b'index'),
    methods=['GET'])
