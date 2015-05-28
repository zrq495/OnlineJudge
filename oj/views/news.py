# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import (views,
                   request,
                   Blueprint,
                   current_app,
                   render_template)

from oj.models import NewsModel


class NewsView(views.MethodView):

    def get(self):
        per_page = current_app.config['NEWS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination = (
            NewsModel.query
            .order_by(NewsModel.date_created.desc())
            .paginate(
                page, per_page=per_page, error_out=False))
        news = pagination.items
        return render_template(
            'news_list.html', pagination=pagination,
            news=news)


class NewsDetailView(views.MethodView):

    def get(self, news_id):
        news = NewsModel.query.get_or_404(news_id)
        return render_template(
            'news_detail.html',
            news=news)


bp_news = Blueprint('news', __name__)
bp_news.add_url_rule(
    '/',
    endpoint='list',
    view_func=NewsView.as_view(b'list'),
    methods=['GET'])
bp_news.add_url_rule(
    '/<int:news_id>/',
    endpoint='detail',
    view_func=NewsDetailView.as_view(b'detail'),
    methods=['GET'])
