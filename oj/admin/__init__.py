# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import redirect, url_for, request
from flask.ext.login import current_user
from flask.ext.admin import Admin, AdminIndexView as _AdminIndexView
from flask.ext.admin.base import MenuLink


class AdminIndexView(_AdminIndexView):
    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login', next=request.url))


flask_admin = Admin(
    name='SDUT OJ后台', index_view=AdminIndexView(name='主页'),
    template_mode='admin')

flask_admin.add_link(MenuLink(name='返回首页', endpoint='index.index'))
flask_admin.add_link(MenuLink(name='注销', endpoint='auth.logout'))

from . import user  # noqa
from . import problem  # noqa
from . import contest  # noqa
from . import news  # noqa
from . import solution  # noqa
from . import file_manager  # noqa
from . import registry  # noqa
