# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oj import db
from oj.models import NewsModel, HeadlineModel
from .mixin import Mixin
from . import flask_admin


class NewsAdmin(Mixin):

    column_exclude_list = ['content']
    column_searchable_list = ['title', 'content']
    column_filters = [
        'id', 'user_id', 'title', 'is_display', 'date_created'
    ]
    column_editable_list = ['is_display']

    form_excluded_columns = ['user_id', 'date_created']

    def __init__(self, session, **kwargs):
        super(NewsAdmin, self).__init__(NewsModel, session, **kwargs)


class HeadlineAdmin(Mixin):

    column_exclude_list = ['url']
    column_searchable_list = ['title', 'url', 'alert']
    column_filters = [
        'id', 'user_id', 'title', 'url', 'alert', 'is_display', 'date_created'
    ]
    column_editable_list = ['is_display']

    form_excluded_columns = ['user_id', 'date_created']

    def __init__(self, session, **kwargs):
        super(HeadlineAdmin, self).__init__(HeadlineModel, session, **kwargs)


flask_admin.add_view(NewsAdmin(
    db.session, name='新闻列表', category='新闻管理', url='news'))
flask_admin.add_view(HeadlineAdmin(
    db.session, name='滚动条列表', category='新闻管理', url='headline'))
