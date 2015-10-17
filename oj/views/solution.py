# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   abort,
                   request,
                   url_for,
                   redirect,
                   Blueprint,
                   current_app,
                   render_template)
from flask.ext.login import login_required, current_user

from oj.models import (
    SolutionModel, CodeModel, CompileInfoModel, UserModel, ContestModel)
from . import forms
from .contest import bp_contest


class SolutionView(views.MethodView):

    template = 'solution_list.html'

    def get(self, is_contest=False):
        form = forms.SolutionSearchForm(request.args, csrf_enabled=False)
        if not form.validate():
            redirect(url_for('solution.list'))
        problem_id = form.problem_id.data
        solution_id = form.solution_id.data
        contest_id = form.contest_id.data
        username = form.username.data
        language = form.language.data
        result = form.result.data
        query = SolutionModel.query
        contest = None
        if is_contest:
            query = query.filter(
                SolutionModel.contest_id != 0)
            if contest_id:
                query = query.filter(
                    SolutionModel.contest_id == contest_id)
                contest = ContestModel.query.get(contest_id)
        else:
            query = query.filter(
                SolutionModel.contest_id == 0)
        if problem_id:
            query = query.filter(
                SolutionModel.problem_id == problem_id)
        if solution_id:
            query = query.filter(
                SolutionModel.id == solution_id)
        if username:
            query = query.filter(
                UserModel.id == SolutionModel.user_id,
                UserModel.username.ilike('%%%s%%' % username))
        if language:
            query = query.filter(
                SolutionModel.program_language == language)
        if result == 0 or result:
            query = query.filter(
                SolutionModel.result == result)
        if problem_id or solution_id or username or language or result:
            return render_template(
                self.template, form=form,
                solutions=query.all())
        per_page = current_app.config['SOLUTIONS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            query
            .order_by(SolutionModel.id.desc())
            .paginate(
                page, per_page=per_page, error_out=False))
        solutions = pagination.items
        SOLUTION_RESULT = current_app.config['SOLUTION_RESULT']
        return render_template(
            self.template, pagination=pagination,
            SOLUTION_RESULT=SOLUTION_RESULT,
            solutions=solutions, form=form, contest=contest)


class CodeDetailView(views.MethodView):

    template = 'code_detail.html'

    @login_required
    def get(self, code_id):
        code = CodeModel.query.get_or_404(code_id)
        if current_user.id != code.solution.user_id and not current_user.is_administrator():
            abort(404)
        SOLUTION_RESULT = current_app.config['SOLUTION_RESULT']
        return render_template(
            self.template, code=code, solution=code.solution,
            SOLUTION_RESULT=SOLUTION_RESULT)


class CompileInfoDetailView(views.MethodView):

    template = 'compile_info_detail.html'

    @login_required
    def get(self, compile_info_id):
        compile_info = CompileInfoModel.query.get_or_404(compile_info_id)
        return render_template(
            self.template, compile_info=compile_info)


bp_solution = Blueprint('solution', __name__)
bp_solution.add_url_rule(
    '/',
    endpoint='list',
    view_func=SolutionView.as_view(b'list'),
    methods=['GET'])

bp_code = Blueprint('code', __name__)
bp_code.add_url_rule(
    '/<int:code_id>/',
    endpoint='detail',
    view_func=CodeDetailView.as_view(b'detail'),
    methods=['GET'])

bp_compile_info = Blueprint('compile_info', __name__)
bp_compile_info.add_url_rule(
    '/<int:compile_info_id>/',
    endpoint='detail',
    view_func=CompileInfoDetailView.as_view(b'detail'),
    methods=['GET'])


bp_contest.add_url_rule(
    '/solution/',
    endpoint='solution',
    view_func=SolutionView.as_view(b'solution'),
    defaults={'is_contest': True},
    methods=['GET'])
