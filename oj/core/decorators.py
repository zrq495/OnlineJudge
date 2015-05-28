# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from functools import wraps
from flask import abort
from flask.ext.login import current_user

from oj.models import Permission


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
