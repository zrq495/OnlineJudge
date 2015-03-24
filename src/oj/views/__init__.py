# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .index import bp_index
from .auth import bp_auth
from .profile import bp_profile
from .problem import bp_problem


__all__ = [
    'bp_index',
    'bp_auth',
    'bp_profile',
    'bp_problem',
]

