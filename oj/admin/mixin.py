# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import redirect, url_for, request
from flask.ext.login import current_user
from flask.ext.admin import form, BaseView
from flask.ext.admin.actions import action
from flask.ext.admin.contrib.sqla import ModelView


labels = dict(
    id='ID',
    name='名称',
    date_updated='更新时间',
    school='学校',
    introduction='简介',
    date_created='数据库创建时间',
    status='状态',
    depts='所在专业',
    content='内容',
    title='标题',
    deleted_by_admin='管理员删除',
    deleted_by_user='用户删除',
    ordinal='序号',
)


def image_validate(form, field):
    field.data = field.data if field.data else None
    #  将''替换为None,否则postgres的CHAR(50)有space padding.


class ModelViewMixin(ModelView):
    column_labels = labels
    form_base_class = form.BaseForm
    column_display_pk = True
    form_extra_fields = None

    column_formatters = dict(
        date_created=(
            lambda v, c, m, p: m.date_created.strftime('%Y-%m-%d %H:%M:%S')),
        date_start=(
            lambda v, c, m, p: m.date_start.strftime('%Y-%m-%d %H:%M:%S')),
        date_end=(
            lambda v, c, m, p: m.date_end.strftime('%Y-%m-%d %H:%M:%S'))
    )

    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login', next=request.url))

    def delete_model(self, model):
        class_ = model.__class__
        if hasattr(class_, 'deleted'):
            self.session.flush()
            self.session.delete(model, reason='deleted_by_admin')
            self.session.commit()
        else:
            super(ModelViewMixin, self).delete_model(model)

    @action('delete', '删除', '确定选中的删除吗')
    def action_delete(self, ids):
        model = self.model
        if hasattr(model, 'deleted'):
            self.session.flush()
            if ids:
                for m in model.query.filter(model.id.in_(ids)).all():
                    self.session.delete(m, reason='deleted_by_admin')
            self.session.commit()
        else:
            super(ModelViewMixin, self).action_delete(ids)

    @action('restore', '恢复', '确定要恢复已经删除的吗')
    def action_restore(self, ids):
        model = self.model
        if model.__tablename__.endswith('deleted'):
            self.session.flush()
            if ids:
                for m in model.query.filter(model.id.in_(ids)).all():
                    m.restore()
            self.session.commit()

    def is_action_allowed(self, name):
        if name == 'restore':
            if hasattr(self, 'can_restore') and self.can_restore:
                return True
            return False
        return super(ModelViewMixin, self).is_action_allowed(name)


class BaseViewMixin(BaseView):
    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login', next=request.url))
