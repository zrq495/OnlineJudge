# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from functools import wraps
from flask import abort, session, redirect, url_for, request
from flask.ext.login import current_user

from oj.models import Permission, ContestModel


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


def contest_access_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        contest = ContestModel.query.get_or_404(kwargs.get('contest_id'))
        if contest.type == 'private' and not \
                session.setdefault('contests', {}).get(str(contest.id), False):
            return redirect(url_for(
                'contest.access_required', contest_id=contest.id,
                next=request.url))
        return func(*args, **kwargs)
    return decorated_view
