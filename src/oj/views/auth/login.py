# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from flask import (
    render_template, redirect, request, url_for, flash, views)
from flask.ext.login import (
    login_user, logout_user, login_required, current_user)

from oj import db
from oj.models import UserModel
from .forms import LoginForm


class LoginView(views.MethodView):

    template = 'auth/login.html'

    def get(self):
        if current_user.is_authenticated():
            return redirect(url_for('index.index'))
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if not form.validate():
            return render_template(
                self.template, form=form)
        query = UserModel.query
        user = (query.filter_by(email=form.login_name.data).first()
                or query.filter_by(username=form.login_name.data).first())
        if user is not None and user.verify_password(form.password.data):
            user_login(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index.index'))
        flash('用户名或密码不正确')
        return render_template(self.template, form=form)


def user_login(user, remember_me=False):
    login_user(user, remember_me)

    if 'X-Forwarded-For' not in request.headers:
        remote_addr = request.remote_addr or 'untrackable'
    else:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0]

    old_current_login, new_current_login = user.date_current_login, datetime.now()
    old_current_ip, new_current_ip = user.current_login_ip, remote_addr

    user.date_last_login = old_current_login or new_current_login
    user.date_current_login = new_current_login
    user.last_login_ip = old_current_ip or new_current_ip
    user.current_login_ip = new_current_ip
    user.login_count = user.login_count + 1 if user.login_count else 1
    db.session.commit()
