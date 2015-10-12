# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from collections import OrderedDict
from flask import (views,
                   flash,
                   request,
                   url_for,
                   redirect,
                   Blueprint,
                   current_app,
                   render_template)
from flask.ext.login import login_required, current_user
from werkzeug.datastructures import MultiDict
from werkzeug.utils import cached_property

from oj.models import (
    ContestModel, ContestProblemModel, ContestUserModel,
    SolutionModel, CodeModel)
from oj import db
from oj.core import timelimit
from . import forms


class ContestView(views.MethodView):

    def get(self):
        per_page = current_app.config['CONTESTS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            ContestModel.query
            .order_by(ContestModel.date_start.desc())
            .paginate(
                page, per_page=per_page, error_out=False))
        contests = pagination.items
        return render_template(
            'contest_list.html', pagination=pagination,
            contests=contests)


class ContestDetailView(views.MethodView):

    def get(self, contest_id):
        now = datetime.datetime.now()
        contest = ContestModel.query.get_or_404(contest_id)
        return render_template(
            'contest_detail.html',
            contest=contest, now=now)


class ContestProblemDetailView(views.MethodView):

    def get(self, contest_problem_id):
        contest_problem = ContestProblemModel.query.get_or_404(
            contest_problem_id)
        problem = contest_problem.problem
        contest = contest_problem.contest
        return render_template(
            'contest_problem_detail.html', problem=problem,
            contest_problem=contest_problem, contest=contest)

    @login_required
    def post(self, contest_problem_id):
        contest_problem = ContestProblemModel.query.get_or_404(
            contest_problem_id
        )
        form = forms.ContestSubmitForm(request.form)
        if self.submit_timeout.get():
            flash('提交过于频繁，请稍候')
            return redirect(
                url_for(
                    'contest.contest_problem',
                    contest_problem_id=contest_problem_id))
        if not form.validate():
            return redirect(
                url_for(
                    'contest.contest_problem',
                    contest_problem_id=contest_problem_id))
        solution = SolutionModel(
            problem_id=contest_problem.problem_id,
            user=current_user._get_current_object(),
            contest_id=contest_problem.contest_id,
            length=len(form.code.data),
            program_language=form.language.data)
        solution.code = CodeModel(
            content=form.code.data)
        db.session.add(solution)
        db.session.commit()
        self.submit_timeout.set()
        return redirect(
            url_for('contest.solution', contest_id=contest_problem.contest_id))

    @cached_property
    def submit_timeout(self):
        _tm = timelimit.TimeLimit(
            'submit', current_app.config.get('SUBMIT_TIMELIMIT', 1))
        return _tm


class ContestRankView(views.MethodView):

    template = 'contest_rank.html'

    def get(self, contest_id):
        rank = OrderedDict()
        contest = ContestModel.query.get_or_404(contest_id)
        contest_problems = contest.problems
        contest_solutions = (
            contest.solutions
            .order_by(
                SolutionModel.user_id.asc(),
                SolutionModel.date_created.asc()))

        for s in contest_solutions:
            if s.result == 1:
                rank.setdefault(s.user_id, {}).setdefault(s.problem_id, {}).setdefault('is_solved', True)
                rank.setdefault(s.user_id, {}).setdefault(s.problem_id, {}).setdefault('solution', s)
            else:
                error_count = rank.setdefault(s.user_id, {}).setdefault(s.problem_id, {}).setdefault('error_count', 0)
                rank[s.user_id][s.problem_id]['error_count'] = error_count + 1
            rank.setdefault(s.user_id, {}).setdefault('user', s.user)
        for r in rank.keys():
            accept_problems = []
            for i in rank[r].keys():
                rank[r].setdefault('accepts_count', 0)
                if isinstance(i, int) and isinstance(rank[r][i], dict):
                    if rank[r][i].get('is_solved', False):
                        penalty = rank[r][i].setdefault('penalty', rank[r][i]['solution'].date_created - contest.date_start)
                        rank[r][i]['penalty'] = penalty + datetime.timedelta(minutes=20) * rank[r][i].get('error_count', 0)
                        if i not in accept_problems:
                            rank[r]['accepts_count'] += 1
                            accept_problems.append(i)
                        rank[r][i].setdefault('error_count', 0)
                    else:
                        rank[r][i].setdefault('penalty', datetime.timedelta(0))
                        rank[r][i].setdefault('is_solved', False)
            for i in rank[r].keys():
                if isinstance(i, int) and isinstance(rank[r][i], dict):
                    rank[r].setdefault('penalties', datetime.timedelta(0))
                    rank[r]['penalties'] += rank[r][i]['penalty']
        rank = OrderedDict(sorted(rank.iteritems(), key=lambda x: x[1]['penalties']))
        rank = OrderedDict(sorted(rank.iteritems(), key=lambda x: x[1]['accepts_count'], reverse=True))

        return render_template(
            self.template, rank=rank, contest=contest,
            contest_problems=contest_problems)


bp_contest = Blueprint('contest', __name__)
bp_contest.add_url_rule(
    '/',
    endpoint='list',
    view_func=ContestView.as_view(b'list'),
    methods=['GET'])
bp_contest.add_url_rule(
    '/<int:contest_id>/',
    endpoint='detail',
    view_func=ContestDetailView.as_view(b'detail'),
    methods=['GET'])
bp_contest.add_url_rule(
    '/problem/<int:contest_problem_id>/',
    endpoint='contest_problem',
    view_func=ContestProblemDetailView.as_view(b'contest_problem'),
    methods=['GET', 'POST'])
bp_contest.add_url_rule(
    '/<int:contest_id>/rank/',
    endpoint='rank',
    view_func=ContestRankView.as_view(b'rank'),
    methods=['GET'])
