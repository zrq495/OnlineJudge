# -*-coding: utf-8 -*-

import re

from flask import g
from flask import current_app as app

from .helpers import cache_for_with_self

__all__ = ['censor']


class CensorCenter(object):

    @cache_for_with_self(60, lambda self: 1)
    def get_name_forbidden_words_pattern(self):
        from oj.models import RegistryModel
        if hasattr(g, '_name_forbidden_words_pattern'):
            return g._name_forbidden_words_pattern
        words = set()
        values = RegistryModel.fetch('name_forbidden_words')
        for row in values:
            is_enabled = row.pop('is_enabled', False)
            if is_enabled:
                words.update([v for v in row.values() if v])
        words = map(lambda w: w.replace('|', '\|').replace('.', '\.'), words)
        g._name_forbidden_words_pattern = pattern = re.compile('|'.join(words))
        return pattern

    def has_name_forbidden_word(self, content):
        if not content or app.config['TESTING']:
            return False
        pattern = self.get_name_forbidden_words_pattern()
        if re.search(pattern, content):
            return True
        return False


censor = CensorCenter()
