#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

import redis

from oj import app

REDIS_URL = app.config['REDIS_URL']
redis = redis.StrictRedis.from_url(REDIS_URL)
