# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint

bp_auth = Blueprint('auth', __name__)

from .signup import SignupView
from .login import LoginView
from .logout import LogoutView


bp_auth.add_url_rule(
    '/signup/',
    endpoint='signup',
    view_func=SignupView.as_view(b'signup'),
    methods=['POST', 'GET']
)
bp_auth.add_url_rule(
    '/login/',
    endpoint='login',
    view_func=LoginView.as_view(b'login'),
    methods=['POST', 'GET']
)
bp_auth.add_url_rule(
    '/logout/',
    endpoint='logout',
    view_func=LogoutView.as_view(b'logout'),
    methods=['GET']
)


from . import password  # noqa
from . import confirm  # noqa
from . import email  # noqa
