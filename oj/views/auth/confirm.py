# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    request, redirect, url_for, flash, render_template)
from flask.ext.login import current_user, login_required
from oj.models import UserModel
from oj.core.tasks import send_email
from . import bp_auth


@bp_auth.before_app_request
def before_request():
    if current_user.is_authenticated():
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and not request.endpoint.endswith('static'):
            return redirect(url_for('auth.unconfirmed'))


@bp_auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('index.index'))


@bp_auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('index.index'))
    return render_template('auth/unconfirmed.html')


@bp_auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    user = UserModel.query.filter_by(email=current_user.email).first()
    send_email.delay(
        user.email,
        'Confirm Your Account',
        'auth/email/confirm',
        user=user, token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('index.index'))
