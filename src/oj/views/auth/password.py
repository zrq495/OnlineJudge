# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    render_template, redirect, request, url_for, flash, views)
from flask.ext.login import (
    login_user, logout_user, login_required, current_user)

from oj import db
from oj.models import UserModel
from oj.core.email import send_email
from . import forms
from . import bp_auth


@bp_auth.route('/change-password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已经更新')
            return redirect(url_for('index.index'))
        else:
            flash('密码不正确')
    return render_template("auth/change_password.html", form=form)


@bp_auth.route('/reset/', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous():
        return redirect(url_for('index.index'))
    form = forms.PasswordResetRequestForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置密码',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            flash('重置密码的邮件已经发到邮箱，请尽快登陆邮箱重置密码')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp_auth.route('/reset/<token>/', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('index.index'))
    form = forms.PasswordResetForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('index.index'))
        if user.reset_password(token, form.password.data):
            flash('密码已经更新')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('index.index'))
    return render_template('auth/reset_password.html', form=form)
