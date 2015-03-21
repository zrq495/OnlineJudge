# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    render_template, redirect, request, url_for, flash, views)
from flask.ext.login import (
    login_user, logout_user, login_required, current_user)
from oj import db, login_manager
from oj.models import UserModel
from oj.core.email import send_email
from .forms import SignupForm


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class SignupView(views.MethodView):

    template = 'auth/signup.html'

    def get(self):
        form = SignupForm()
        return render_template(self.template, form=form)

    def post(self):
        form = SignupForm()
        if not form.validate():
            return render_template(
                self.template, form=form), 400
        user = UserModel()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
