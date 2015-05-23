# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    render_template, redirect, request, url_for, flash, views)
from flask.ext.login import (
    login_user, logout_user, login_required, current_user)


class LogoutView(views.MethodView):

    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('index.index'))
