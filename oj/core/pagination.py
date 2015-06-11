# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import ceil


class ProblemPagination(object):

    def __init__(self, page, per_page, total_count, max_id, start_id=1000):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.max_id = max_id
        self.start_id = start_id

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def pages(self):
        return int(ceil((self.max_id - self.start_id + 1) / float(self.per_page)))

    @property
    def next_num(self):
        return self.page + 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self):
        for num in xrange(1, self.pages + 1):
            yield num
