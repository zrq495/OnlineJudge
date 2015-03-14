# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask.ext.restful import Resource

from oj.blueprints import api


class HelloWorld(Resource):
    def get(self):
        return {
            'HELLO': 'WORLD',
        }

api.add_resource(HelloWorld, '/hello/')
