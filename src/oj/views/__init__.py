# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .index import bp_index
from .auth import bp_auth
from .profile import bp_profile
from .problem import bp_problem
from .news import bp_news
from .solution import bp_solution


__all__ = [
    'bp_index',
    'bp_auth',
    'bp_profile',
    'bp_problem',
    'bp_news',
    'bp_solution',
]

