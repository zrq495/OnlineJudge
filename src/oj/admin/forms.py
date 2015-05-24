# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import g
from flask.ext.wtf import Form, file
from wtforms import Form as WTForm
from wtforms import fields, validators, ValidationError


class ExcelUploadForm(Form):
    upload_file = file.FileField(
        'excel文件',
        validators=[file.FileRequired(message='这不是一个文件')])
    submit = fields.SubmitField('Submit')


class RegistryMetaForm(WTForm):
    kind = fields.SelectField(
        '字段类型',
        choices=(('int', '整型'),
                 ('bool', '布尔'),
                 ('string', '字符串'),
                 ('url', 'URL')),
        description='选择字段类型',
        validators=[validators.Required('字段类型必选')])
    name = fields.StringField(
        '字段名称',
        description='字段名称',
        validators=[validators.Required('字段名称必填')])
    label = fields.StringField(
        '中文名',
        description='字段中文名',
        validators=[validators.Required('字段中文名必填')])
    required = fields.BooleanField(
        '必填',
        description='是否必填',
        default=True)


class EditRegistryMetaForm(Form):
    key = fields.StringField(
        '关键字',
        description='输入关键字',
        validators=[validators.Required('关键字不能为空')])
    name = fields.StringField(
        '中文名称',
        description='输入中文名称',
        validators=[validators.Required('中文名称不能为空')])
    meta = fields.FieldList(
        fields.FormField(RegistryMetaForm),
        default=[{}])

    def validate_key(self, field):
        from oj.models import RegistryModel
        if g.registry and g.registry.key == field.data:
            return
        if RegistryModel.query.get(field.data):
            raise ValidationError('关键字已存在')

    def validate_meta(self, fields):
        names = [f['name'] for f in fields.data]
        if not names:
            raise ValidationError('不能没有字段啊')
        if len(names) != len(set(names)):
            raise ValidationError('字段英文名不能重复')
