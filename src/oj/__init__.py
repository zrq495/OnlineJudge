# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

from config import config
from oj.core.sqlalchemy import SQLAlchemy

import os
app_dir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['APP_DIR'] = app_dir


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .admin import flask_admin
    flask_admin.init_app(app)

    from .core.jinja import JINJA_FILTERS
    app.jinja_env.filters.update(JINJA_FILTERS)

    from oj.blueprints import blueprint_apis
    from . import apis  # noqa
    from .views import (
        bp_index,
        bp_auth,
        bp_profile,
        bp_problem,
        bp_news,
        bp_solution,
        bp_code,
        bp_compile_info,
        bp_rank,
        bp_contest,
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

    app.register_blueprint(
        bp_news,
        url_prefix='/news')

    app.register_blueprint(
        bp_solution,
        url_prefix='/solution')

    app.register_blueprint(
        bp_code,
        url_prefix='/code')

    app.register_blueprint(
        bp_compile_info,
        url_prefix='/compile')

    app.register_blueprint(
        bp_rank,
        url_prefix='/rank')

    app.register_blueprint(
        bp_contest,
        url_prefix='/contest')

    from .models import Permission

    @app.context_processor
    def inject_permissions():
        return dict(Permission=Permission)

    return app
