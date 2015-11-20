# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint

bp_profile = Blueprint('profile', __name__)

from .profile import ProfileView


bp_profile.add_url_rule(
    '/u/<int:user_id>/',
    endpoint='profile',
    view_func=ProfileView.as_view(b'profile'),
    methods=['GET']
)
