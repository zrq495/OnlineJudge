# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask.ext.login import current_user
from flask.ext.admin import Admin, AdminIndexView as _AdminIndexView


class AdminIndexView(_AdminIndexView):
    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())


flask_admin = Admin(
    name='SDUT OJ后台', index_view=AdminIndexView(name='主页'), template_mode='bootstrap3')

from . import user  # noqa
from . import problem  # noqa
from . import contest  # noqa
from . import news  # noqa
from . import solution  # noqa
from . import file_manager  # noqa
from . import registry  # noqa
