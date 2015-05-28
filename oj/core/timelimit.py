# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from oj.core.cache import redis
from flask import current_app as app
from flask.ext.login import current_user


class TimeLimit(object):

    def __init__(self, key, timeout, prefix='timelimit'):
        """
        Parameter:
            timeout: 单位秒
        """
        self.rkey = '%s:%s:%s' % (prefix, key, current_user.get_id())
        self.timeout = timeout

    def set(self):
        """
        :Returns:
            True: 设置成功
            False: 设置失败

        """
        enable = app.config.get('ENABLE_TIMELIMIT', True)

        if app.config['TESTING']:
            enable = False

        if app and not enable:
            return True

        value = redis.get(self.rkey)
        if value:
            return False
        with redis.pipeline() as rp:
            rp.set(self.rkey, self.timeout)
            rp.expire(self.rkey, self.timeout)
            setted, _ = rp.execute()
        return setted

    def get(self):
        """
        :Returns:
            True: 已经设置
            False: 没有设置
        """
        enable = app.config.get('ENABLE_TIMELIMIT', True)
        if app.config['TESTING']:
            enable = False

        if app and not enable:
            return False
        return True if redis.get(self.rkey) else False
