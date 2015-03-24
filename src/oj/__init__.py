# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

from config import config
from oj.core.sqlalchemy import SQLAlchemy


mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()
flask_admin = Admin(name='SDUT OJ')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__)
app.config.from_object('config')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    flask_admin.init_app(app)

    from oj.blueprints import blueprint_apis
    from . import apis  # noqa
    from . import admin  # noqa
    from .views import (
        bp_index,
        bp_auth,
        bp_profile,
        bp_problem,
    )

    app.register_blueprint(
        blueprint_apis,
        url_prefix='/api')

    app.register_blueprint(
        bp_index,
        url_prefix='/')

    app.register_blueprint(
        bp_auth,
        url_prefix='/auth')

    app.register_blueprint(
        bp_profile,
        url_prefix='')

    app.register_blueprint(
        bp_problem,
        url_prefix='/problem')

    return app
