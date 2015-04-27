# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask.ext.wtf import Form, file
from wtforms import fields


class ExcelUploadForm(Form):
    upload_file = file.FileField(
        'excel文件',
        validators=[file.FileRequired(message='这不是一个文件')])
    submit = fields.SubmitField('Submit')
