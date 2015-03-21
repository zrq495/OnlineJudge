# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint

bp_profile = Blueprint('profile', __name__)

from .profile import ProfileView
from .edit import ProfileEditView


bp_profile.add_url_rule(
    '/u/<int:user_id>/',
    view_func=ProfileView.as_view(b'profile'),
    methods=['GET']
)
bp_profile.add_url_rule(
    '/setting/',
    view_func=ProfileEditView.as_view(b'setting'),
    methods=['POST', 'GET']
)
