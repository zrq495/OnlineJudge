# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict
from flask import (
    views, render_template, request,
    redirect, url_for, g)
from flask.ext.wtf import Form
from flask.ext.login import current_user
from flask.ext.admin import expose, expose_plugview, BaseView
from wtforms import Form as WTForm
from wtforms import fields, validators
from wtforms.fields import html5
from werkzeug.exceptions import NotFound

from oj import db
from oj.models import RegistryModel
from . import flask_admin
from . import forms
from .mixin import Mixin


class RegistryAdmin(Mixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['key', 'name']

    list_template = 'admin/registry_list.html'

    def __init__(self, session, **kwargs):
        super(RegistryAdmin, self).__init__(RegistryModel, session, **kwargs)


class RegistryView(BaseView):

    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return redirect(url_for('registrymodel.index_view'))

    @expose_plugview('/edit_meta/<string:key>/')
    @expose_plugview('/edit_meta/')
    class EditRegistryMetaView(views.MethodView):

        template = 'admin/edit_registry_meta.html'

        def _get_registry(self, key):
            registry = None
            if key:
                registry = RegistryModel.query.get(key)
                if not registry:
                    raise NotFound('没有这个注册项')
            return registry

        def get(self, cls, key=None):
            print request.endpoint
            registry = self._get_registry(key)
            form = forms.EditRegistryMetaForm(obj=registry)
            return cls.render(self.template, form=form)

        def error(self, registry, form, cls):
            return cls.render(
                self.template, registry=registry, form=form), 400

        def post(self, cls, key=None):
            registry = self._get_registry(key)
            g.registry = registry
            form = forms.EditRegistryMetaForm(request.form)
            if not form.validate():
                return self.error(registry, form, cls)
            if not registry:
                db.session.add(
                    RegistryModel(key=form.key.data,
                                  name=form.name.data,
                                  meta=form.meta.data,
                                  value=[]))
            else:
                registry.key = form.key.data
                registry.name = form.name.data
                registry.meta = form.meta.data
            db.session.commit()
            return redirect(url_for('.index'))

    @expose_plugview('/edit_value/<string:key>/')
    class EditRegistryValueView(views.MethodView):

        template = 'admin/edit_registry_value.html'
        default_values = {
            'int': 0,
            'bool': False,
            'string': '',
            'url': ''}

        def _get_registry(self, key):
            if key:
                registry = RegistryModel.query.get(key)
                if registry:
                    return registry
            raise NotFound('没有这个注册项')

        def get(self, cls, key=None):
            registry = self._get_registry(key)
            form_class = construct_form(registry.meta)
            form = form_class(obj=registry)
            return cls.render(self.template, form=form)

        def error(self, registry, form, cls):
            return cls.render(self.template, form=form), 400

        def post(self, cls, key):
            registry = self._get_registry(key)
            form_class = construct_form(registry.meta)
            form = form_class(request.form)
            if not form.validate():
                return self.error(registry, form, cls)
            value = form.value.data
            meta = registry.meta
            for define in meta:
                for v in value:
                    if define['name'] not in v:
                        v[define['name']] = self.default_values[define['type']]
            registry.value = value
            db.session.commit()
            registry.save_to_cache()
            return redirect(url_for('.index'))


def construct_form(meta):
    subfs = OrderedDict()
    for field in meta:
        kind = field['kind']
        name = field['name']
        label = field['label']
        required = field['required']
        checkers = []
        if required:
            if kind == 'int':
                checkers.append(validators.InputRequired('这个字段必填'))
            else:
                checkers.append(validators.Required('这个字段必填'))
        else:
            checkers.append(validators.Optional())
        if kind == 'int':
            f = html5.IntegerField(
                label,
                description='输入' + label,
                validators=checkers)
        elif kind == 'bool':
            f = fields.BooleanField(
                label,
                description=label,
                validators=[validators.Optional()])
        elif kind == 'string':
            f = fields.StringField(
                label,
                description='输入' + label,
                validators=checkers)
        elif kind == 'url':
            checkers.append(validators.URL())
            f = html5.URLField(
                label,
                description='输入' + label,
                validators=checkers)
        else:
            raise NotImplementedError('%s kind not supported' % kind)
        subfs[name] = f
    subform_class = type(b'_Registry_Sub_Form', (WTForm, ), subfs)
    value_field = fields.FieldList(
        fields.FormField(subform_class),
        default=[{}])
    form_class = type(b'_Registry_Form', (Form, ),
                      OrderedDict(value=value_field))
    return form_class


flask_admin.add_view(RegistryAdmin(
    db.session, name='注册表', url='registry'))
flask_admin.add_view(RegistryView(name='编辑注册表', url='edit_registry'))
