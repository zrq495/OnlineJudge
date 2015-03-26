# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   request,
                   url_for,
                   redirect,
                   Blueprint,
                   current_app,
                   render_template)

from oj.models import (
    SolutionModel, CodeModel, CompileInfoModel, UserModel)
from . import forms


class SolutionView(views.MethodView):

    template = 'solution_list.html'

    def get(self):
        form = forms.SolutionSearchForm(request.args, csrf_enabled=False)
        if not form.validate():
            redirect(url_for('solution.list'))
        problem_id = form.problem_id.data
        solution_id = form.solution_id.data
        username = form.username.data
        language = form.language.data
        result = form.result.data
        query = SolutionModel.query
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
        if result:
            query = query.filter(
                SolutionModel.result == result)
        if problem_id or solution_id or username or language or result:
            return render_template(
                self.template, form=form,
                solutions=query.all())
        per_page = current_app.config['SOLUTIONS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            SolutionModel.query
            .order_by(SolutionModel.id.asc())
            .paginate(
                page, per_page=per_page, error_out=False))
        solutions = pagination.items
        return render_template(
            self.template, pagination=pagination,
            solutions=solutions, form=form)


bp_solution = Blueprint('solution', __name__)
bp_solution.add_url_rule(
    '/',
    endpoint='list',
    view_func=SolutionView.as_view(b'list'),
    methods=['GET'])
