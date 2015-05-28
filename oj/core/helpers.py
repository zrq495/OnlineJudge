# -*-coding:utf-8 -*-

from __future__ import unicode_literals

import time
import pickle
from functools import wraps

from flask import current_app as app


__all__ = ['cache_for', 'cache_for_with_self']


def cache_for(duration):
    def deco(func):
        @wraps(func)
        def fn(*args, **kwargs):
            if app.testing:
                return func(*args, **kwargs)

            key = pickle.dumps((args, kwargs))

            value, expire = func.func_dict.get(key, (None, None))
            now = int(time.time())
            if value is not None and expire > now:
                return value
            value = func(*args, **kwargs)
            func.func_dict[key] = (value, int(time.time()) + duration)
            return value
        return fn
    return deco


def cache_for_with_self(duration, attr_or_callable):
    def deco(func):
        @wraps(func)
        def fn(self, *args, **kwargs):
            if app.testing:
                return func(self, *args, **kwargs)
            if isinstance(attr_or_callable, basestring):
                self_id = getattr(self, attr_or_callable)
            else:
                self_id = attr_or_callable(self)
            all_args = [self_id]
            all_args.extend(args)
            key = pickle.dumps((all_args, kwargs))
            value, expire = func.func_dict.get(key, (None, None))
            now = int(time.time())
            if value is not None and expire > now:
                return value
            value = func(self, *args, **kwargs)
            func.func_dict[key] = (value, int(time.time()) + duration)
            return value
        return fn
    return deco
