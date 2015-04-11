# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   request,
                   url_for,
                   redirect,
                   Blueprint,
                   current_app,
                   render_template)
from flask.ext.login import login_required, current_user
from werkzeug.datastructures import MultiDict

from oj import db
from oj.models import SolutionModel, CodeModel
from . import forms


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
        return redirect(url_for('solution.list'))


bp_submit = Blueprint('submit', __name__)
bp_submit.add_url_rule(
    '/',
    endpoint='submit',
    view_func=SubmitView.as_view(b'submit'),
    methods=['GET', 'POST'])
