#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

import redis

from config import Config

REDIS_URL = Config.REDIS_URL
redis = redis.StrictRedis.from_url(REDIS_URL)
