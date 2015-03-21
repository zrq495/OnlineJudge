# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (
    views,
    render_template,
    abort)
from flask.ext.login import login_required, current_user

from oj.models import UserModel


class ProfileView(views.MethodView):

    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404)

        return render_template(
            'profile/profile.html', user=user)


class UserFavoritesView(views.MethodView):

    @login_required
    def get(self):
        problems = current_user.favorites.all()
        return render_template(
            'favorites.html', problems=problems)
