# -*- coding: utf-8 -*-

from .flask import GuokrFlask

app = GuokrFlask(__name__)

with app.app_context():
    from .views import (
        bp_index,
        bp_board,
        bp_post,
        bp_profile,
        bp_notice,
        bp_search,
        bp_captcha,
        bp_sitemap,
        bp_image,
        bp_message,
        bp_topic,
        bp_tag,
        bp_market,
        bp_feed,
        bp_auth,
        bp_tribe,
    )
    from . import apis, backends  # noqa
    from .blueprints import blueprint_apis, blueprint_backends

    from . import admin
    from .blueprints import blueprint_admin
    admin.register_all()

    app.register_blueprint(
        blueprint_admin, url_prefix='/whosyourdaddy', subdomain='sex')

    app.register_blueprint(
        bp_index,
        url_prefix='/',
        subdomain='sex')
    app.register_blueprint(
        bp_image,
        url_prefix='/image',
        subdomain='sex')
    app.register_blueprint(
        bp_board,
        url_prefix='',
        subdomain='sex')
    app.register_blueprint(
        bp_post,
        url_prefix='/post',
        subdomain='sex')
    app.register_blueprint(
        bp_profile,
        url_prefix='',
        subdomain='sex')
    app.register_blueprint(
        bp_notice,
        url_prefix='/notice',
        subdomain='sex')
    app.register_blueprint(
        bp_search,
        url_prefix='/search',
        subdomain='sex')
    app.register_blueprint(
        blueprint_backends,
        url_prefix='/sex',
        subdomain='backends')
    app.register_blueprint(
        blueprint_apis,
        url_prefix='/sex',
        subdomain='sex')
    app.register_blueprint(
        bp_captcha,
        url_prefix='/captcha',
        subdomain='sex')
    app.register_blueprint(
        bp_sitemap,
        subdomain='sex'
    )
    app.register_blueprint(
        bp_message,
        subdomain='sex', url_prefix='/message'
    )
    app.register_blueprint(
        bp_topic,
        subdomain='sex', url_prefix='/topic'
    )
    app.register_blueprint(
        bp_tag,
        subdomain='sex', url_prefix='/tag'
    )
    app.register_blueprint(
        bp_market,
        subdomain='sex', url_prefix='/market'
    )
    app.register_blueprint(
        bp_feed,
        subdomain='sex',
    )
    app.register_blueprint(
        bp_auth,
        subdomain='sex', url_prefix='/auth'
    )
    app.register_blueprint(
        bp_tribe,
        subdomain='sex', url_prefix='/tribe'
    )

    app.static_folder = 'static'
    app.add_url_rule(
        '/apps/%s/<path:filename>' % app.name,
        endpoint='static',
        subdomain='static',
        view_func=app.send_static_file)
    app.add_url_rule(
        '/apps/%s/<path:filename>' % app.name,
        endpoint='sslstatic',
        subdomain='sslstatic',
        view_func=app.send_static_file)

    app.enable_sso('/sso/sex', ['sex'])

    from sex.views.auth.base import external_signin, get_success
    app.jinja_env.globals.update(
        external_signin=external_signin, get_success=get_success)
