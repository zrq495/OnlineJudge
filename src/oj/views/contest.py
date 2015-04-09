# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from flask import (views,
                   request,
                   url_for,
                   redirect,
                   Blueprint,
                   current_app,
                   render_template)

from oj.models import (
    ContestModel, ContestProblemModel, ContestUserModel)
from . import forms


class ContestView(views.MethodView):

    def get(self):
        per_page = current_app.config['CONTESTS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            ContestModel.query
            .order_by(ContestModel.id.asc())
            .paginate(
                page, per_page=per_page, error_out=False))
        contests = pagination.items
        return render_template(
            'contest_list.html', pagination=pagination,
            contests=contests)


class ProblemDetailView(views.MethodView):

    def get(self, contest_id):
        now = datetime.datetime.now()
        contest = ContestModel.query.get_or_404(contest_id)
        return render_template(
            'contest_detail.html',
            contest=contest, now=now)


bp_contest = Blueprint('contest', __name__)
bp_contest.add_url_rule(
    '/',
    endpoint='list',
    view_func=ContestView.as_view(b'list'),
    methods=['GET'])
bp_contest.add_url_rule(
    '/<int:contest_id>/',
    endpoint='detail',
    view_func=ProblemDetailView.as_view(b'detail'),
    methods=['GET'])
