# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    render_template, redirect, request, url_for, flash, views)
from flask.ext.login import (
    login_user, logout_user, login_required, current_user)
from oj.models import UserModel
from oj.core.email import send_email
from .forms import LoginForm


class LoginView(views.MethodView):

    template = 'auth/login.html'

    def get(self):
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if not form.validate():
            return render_template(
                self.template, form=form)
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index.index'))
        flash('Invalid username or password.')
        return render_template(self.template, form=form)
