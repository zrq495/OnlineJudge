# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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

from oj import db
from oj.models import SolutionModel, CodeModel, ProblemModel
from oj.core import timelimit
from . import forms


class ProblemView(views.MethodView):

    def get(self):
        form = forms.ProblemSearchForm(request.args, csrf_enabled=False)
        if not form.validate():
            redirect(url_for('problem.list'))
        problem_id = form.problem_id.data
        problem_title = form.problem_title.data
        query = ProblemModel.query
        if problem_id:
            query = query.filter(
                ProblemModel.id == problem_id)
        if problem_title:
            query = query.filter(
                ProblemModel.title.ilike('%%%s%%' % problem_title))
        if problem_id or problem_title:
            return render_template(
                'problem_list.html', form=form,
                problems=query.all())
        per_page = current_app.config['PROBLEMS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            query
            .order_by(ProblemModel.id.asc())
            .paginate(
                page, per_page=per_page, error_out=False))
        problems = pagination.items
        return render_template(
            'problem_list.html', pagination=pagination,
            problems=problems, form=form)


class ProblemDetailView(views.MethodView):

    def get(self, problem_id):
        problem = ProblemModel.query.get_or_404(problem_id)
        return render_template(
            'problem_detail.html',
            problem=problem)


class SubmitView(views.MethodView):

    template = 'submit.html'

    @login_required
    def get(self):
        values = MultiDict(request.args)
        values['language'] = current_user.program_language
        form = forms.SubmitForm(values)
        return render_template(self.template, form=form)

    @login_required
    def post(self):
        form = forms.SubmitForm(request.form)
        if self.submit_timeout.get():
            flash('提交过于频繁，请稍候')
            return render_template(
                self.template, form=form)
        if not form.validate():
            return render_template(
                self.template, form=form)
        solution = SolutionModel(
            problem_id=form.problem_id.data,
            user=current_user._get_current_object(),
            length=len(form.code.data),
            program_language=form.language.data)
        solution.code = CodeModel(
            content=form.code.data)
        db.session.add(solution)
        db.session.commit()
        self.submit_timeout.set()
        return redirect(url_for('solution.list'))

    @cached_property
    def submit_timeout(self):
        _tm = timelimit.TimeLimit(
            'submit', current_app.config.get('SUBMIT_TIMELIMIT', 1))
        return _tm


bp_problem = Blueprint('problem', __name__)
bp_problem.add_url_rule(
    '/',
    endpoint='list',
    view_func=ProblemView.as_view(b'list'),
    methods=['GET'])
bp_problem.add_url_rule(
    '/<int:problem_id>/',
    endpoint='detail',
    view_func=ProblemDetailView.as_view(b'detail'),
    methods=['GET'])
bp_problem.add_url_rule(
    '/submit/',
    endpoint='submit',
    view_func=SubmitView.as_view(b'submit'),
    methods=['GET', 'POST'])
