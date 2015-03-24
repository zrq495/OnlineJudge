# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   request,
                   Blueprint,
                   current_app,
                   render_template)

from oj.models import ProblemModel


class ProblemView(views.MethodView):

    def get(self):
        per_page = current_app.config['PROBLEMS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            ProblemModel.query
            .order_by(ProblemModel.id.asc())
            .paginate(
                page, per_page=per_page, error_out=False))
        problems = pagination.items
        return render_template(
            'problem.html',
            pagination=pagination,
            problems=[p.as_dict() for p in problems])


bp_problem = Blueprint('problem', __name__)
bp_problem.add_url_rule(
    '/',
    endpoint='list',
    view_func=ProblemView.as_view(b'list'),
    methods=['GET'])
