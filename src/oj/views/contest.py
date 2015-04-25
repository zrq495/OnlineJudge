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
from flask.ext.login import login_required, current_user
from werkzeug.datastructures import MultiDict

from oj.models import (
    ContestModel, ContestProblemModel, ContestUserModel,
    SolutionModel, CodeModel)
from oj import db
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
        contest_problem = ContestProblemModel.query.get_or_404(contest_problem_id)
        problem = contest_problem.problem
        return render_template(
            'contest_problem_detail.html', problem=problem,
            contest_problem=contest_problem)


class ContestSubmitView(views.MethodView):

    template = 'contest_submit.html'

    @login_required
    def get(self):
        values = MultiDict(request.args)
        values['language'] = current_user.program_language
        form = forms.ContestSubmitForm(values)
        return render_template(self.template, form=form)

    @login_required
    def post(self):
        form = forms.ContestSubmitForm(request.form)
        if not form.validate():
            return render_template(
                self.template, form=form)
        contest_problem = ContestProblemModel.query.get(
            form.contest_problem_id.data)
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
        return redirect(url_for('contest.solution'))


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
    methods=['GET'])
bp_contest.add_url_rule(
    '/problem/submit/',
    endpoint='submit',
    view_func=ContestSubmitView.as_view(b'submit'),
    methods=['GET', 'POST'])
