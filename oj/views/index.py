# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from flask import (views,
                   Blueprint,
                   render_template)
from flask.ext.login import current_user
from sqlalchemy import func, distinct

from oj.models import UserModel, ProblemModel, SolutionModel
from oj import db
from oj.core.helpers import cache_for


class IndexView(views.MethodView):

    def get(self):
        user = current_user._get_current_object()
        day_top = get_days_top(), '今日统计'
        week_top = get_days_top(days=7), '近一周统计'
        month_top = get_days_top(days=30), '近一个月统计'
        year_top = get_days_top(days=365), '近一年统计'
        return render_template(
            'index.html', user=user, day_top=day_top, week_top=week_top,
            month_top=month_top, year_top=year_top)


@cache_for(3600)
def get_days_top(days=1, top=10):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(1)
    users = (
        SolutionModel.query
        .filter(UserModel.id == SolutionModel.user_id)
        .filter(SolutionModel.result == 1)
        .filter(tomorrow - SolutionModel.date_created <= datetime.timedelta(days=days))
        .group_by(UserModel.id)
        .order_by(func.count(distinct(SolutionModel.problem_id)).desc())
        .limit(top)
        .values(func.count(distinct(SolutionModel.problem_id)), UserModel.id, UserModel.username))
    return list(users)


bp_index = Blueprint('index', __name__)
bp_index.add_url_rule(
    '',
    view_func=IndexView.as_view(b'index'),
    methods=['GET'])
