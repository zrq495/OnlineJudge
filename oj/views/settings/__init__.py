# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint
from .profile import EditProfileView
from .email import ChangeEmailView

bp_settings = Blueprint('settings', __name__)


bp_settings.add_url_rule(
    '/profile/',
    endpoint='profile',
    view_func=EditProfileView.as_view(b'profile'),
    methods=['POST', 'GET']
)
bp_settings.add_url_rule(
    '/email/',
    endpoint='email',
    view_func=ChangeEmailView.as_view(b'email'),
    methods=['POST', 'GET']
)
