# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from flask import current_app as app
from sqlalchemy.dialects.postgresql import JSON

from oj import db
from oj.core.cache import redis


__all__ = ['RegistryModel']


class RegistryModel(db.Model):
    __tablename__ = 'registry'

    key = db.Column(db.String(100), nullable=False, primary_key=True)
    name = db.Column(db.Unicode(1024), nullable=False)
    meta = db.Column(JSON, nullable=False, default=[])
    value = db.Column(JSON, default=[])

    def as_dict(self):
        return {
            'key': self.key,
            'name': self.name,
            'value': self.value
        }

    def save_to_cache(self):
        if app.config['TESTING']:
            return
        redis.set(self.redis_key(self.key), json.dumps(self.value))

    @classmethod
    def get_from_cache(cls, key):
        if app.config['TESTING']:
            return
        raw = redis.get(cls.redis_key(key))
        if raw:
            return json.loads(raw)

    @classmethod
    def fetch(cls, key):
        value = cls.get_from_cache(key)
        if value is not None:
            return value
        registry = cls.query.get(key)
        if registry:
            registry.save_to_cache()
            return registry.value
        return []

    @classmethod
    def redis_key(cls, key):
        return 'admin-registry::%s' % key
