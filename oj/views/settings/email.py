# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    views,
    redirect,
    url_for,
    flash,
    render_template)
from flask.ext.login import login_required, current_user

from .forms import ChangeEmailForm
from oj.core.tasks import send_email


class ChangeEmailView(views.MethodView):

    template = 'settings/email.html'
    decorators = [login_required]

    def get(self):
        form = ChangeEmailForm()
        return render_template(self.template, form=form)

    def post(self):
        form = ChangeEmailForm()
        if not form.validate():
            return render_template(self.template, form=form)
        new_email = form.new_email.data
        user = current_user._get_current_object()
        token = current_user.generate_email_change_token(new_email)
        send_email.delay(
            new_email,
            'Confirm your email address',
            'auth/email/change_email',
            user=user,
            token=token
        )
        flash('An email with instructions to confirm your new email '
              'address has been sent to you.')
        return redirect(url_for('settings.email'))
