# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Blueprint
from flask.ext.restful import Api

blueprint_apis = Blueprint('apis', __name__)
api = Api(blueprint_apis)
