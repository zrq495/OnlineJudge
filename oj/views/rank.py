# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   request,
                   url_for,
                   redirect,
                   Blueprint,
                   current_app,
                   render_template)

from oj.models import UserModel, UserStatisticsModel
from . import forms


class RankView(views.MethodView):

    def get(self):
        per_page = current_app.config['RANK_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            UserModel.query
            .outerjoin(
                UserStatisticsModel,
                UserStatisticsModel.id == UserModel.id)
            .order_by(
                UserStatisticsModel.accepts_count.desc(),
                UserStatisticsModel.solutions_count.asc(),
                UserStatisticsModel.id.asc())
            .paginate(
                page, per_page=per_page, error_out=False))
        users = pagination.items
        return render_template(
            'rank_list.html', pagination=pagination,
            users=users, per_page=per_page)


bp_rank = Blueprint('rank', __name__)
bp_rank.add_url_rule(
    '/',
    endpoint='list',
    view_func=RankView.as_view(b'list'),
    methods=['GET'])
