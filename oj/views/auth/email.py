# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    redirect,
    url_for,
    flash)
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from . import bp_auth


class ChangeEmailView(MethodView):

    decorators = [login_required]

    def get(self, token):
        if current_user.change_email(token):
            flash('Your email address has been updated.')
        else:
            flash('Invalid request.')
        return redirect(url_for('auth.login'))

bp_auth.add_url_rule(
    '/change_email/<token>',
    endpoint='change_email',
    view_func=ChangeEmailView.as_view(b'change_email'),
    methods=['get']
)
