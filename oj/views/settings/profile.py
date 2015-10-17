# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    views,
    render_template,
    abort,
    redirect,
    url_for)
from flask.ext.login import login_required, current_user

from oj import db
from .forms import ProfileForm


class EditProfileView(views.MethodView):

    @login_required
    def get(self):
        user = current_user._get_current_object()
        if not user:
            raise abort(404)
        form = ProfileForm(obj=user)
        return render_template(
            'settings/profile.html',
            form=form,
            user=user)

    @login_required
    def post(self):
        user = current_user._get_current_object()
        if not user:
            raise abort(404)

        form = ProfileForm()
        if not form.validate():
            return render_template(
                'settings/profile.html',
                form=form,
                user=user)
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('profile.profile', user_id=user.id))
