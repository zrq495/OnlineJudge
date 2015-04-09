# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def digital_to_letter(value, base='A'):
    try:
        return chr(value % 26 + ord(base))
    except:
        return ''

JINJA_FILTERS = {
    'digital_to_letter': digital_to_letter,
}
