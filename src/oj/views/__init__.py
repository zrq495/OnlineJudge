# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .index import bp_index
from .auth import bp_auth
from .profile import bp_profile
from .problem import bp_problem
from .news import bp_news
from .solution import bp_solution, bp_code, bp_compile_info
from .rank import bp_rank
from .contest import bp_contest
from .submit import bp_submit


__all__ = [
    'bp_index',
    'bp_auth',
    'bp_profile',
    'bp_problem',
    'bp_news',
    'bp_solution',
    'bp_code',
    'bp_compile_info',
    'bp_rank',
    'bp_contest',
    'bp_submit',
]

