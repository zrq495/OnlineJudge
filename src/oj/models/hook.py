# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import event

from oj import db

__all__ = ['entity', 'EntityHook', 'HookCenter']

'''
钩子列表，所有的钩子最终都会在这里
'''
hook_templates = {}


def entity(entity_clazz):
    '''
    钩子的装饰器，钩子函数与实体关联，怎么用见实例就明白了
    '''
    def deco(hook_clazz):
        hook_templates[entity_clazz] = hook_clazz
        return hook_clazz
    return deco


class HookCenter(object):
    '''
    钩子控制器
    '''

    status_list = ['new', 'deleted', 'dirty']

    def get_hookers(self, session):
        hookers = getattr(session, '_hookers', {})
        if hookers:
            return hookers
        setattr(session, '_hookers', hookers)
        for entity_clazz, hooker_clazz in hook_templates.iteritems():
            hookers[entity_clazz] = hooker_clazz()
        return hookers

    def collect_entities(self, session, stage):
        '''
        收集数据实体
        '''
        hookers = self.get_hookers(session)
        for status in self.status_list:
            for obj in getattr(session, status):
                for entity_clazz, hooker in hookers.iteritems():
                    if isinstance(obj, entity_clazz):
                        method = getattr(hooker, 'collect_entities_%s' % stage)
                        method(obj, status)

    def call_hookers(self, session, method_name):
        '''
        以收集的数据实体为参数，调用相关钩子方法
        '''
        hookers = self.get_hookers(session)
        for entity_clazz, hooker in hookers.iteritems():
            method = getattr(hooker, method_name)
            method()

    def after_flush(self, session, context):
        self.collect_entities(session, 'after_flush')

    def before_flush(self, session, context, objects):
        '''
        调用钩子的before_flush方法
        '''
        self.collect_entities(session, 'before_flush')
        self.call_hookers(session, 'before_flush')

    def after_flush_postexec(self, session, context):
        '''
        调用钩子的after_flush_postexec方法
        '''
        self.call_hookers(session, 'after_flush_postexec')

    def after_commit(self, session):
        '''
        调用钩子的after_commit方法
        '''
        self.call_hookers(session, 'after_commit')

    def before_commit(self, session):
        '''
        调用钩子的before_commit方法
        '''
        self.call_hookers(session, 'before_commit')

    def register_events(self):
        event.listen(db.session, 'before_flush', self.before_flush)
        event.listen(db.session, 'after_flush', self.after_flush)
        event.listen(db.session, 'after_flush_postexec',
                     self.after_flush_postexec)
        event.listen(db.session, 'before_commit', self.before_commit)
        event.listen(db.session, 'after_commit', self.after_commit)


class EntityHook(object):
    '''
    钩子基础类，提供常用的方法供钩子调用

    on_commit: 提交后调用
    on_flush: flush后调用
    '''

    pre_flush_interest = []
    flush_interest = ['new', 'deleted']
    commit_interest = []

    def __init__(self):
        self.pre_flush_entities = {}
        self.flush_entities = {}
        self.commit_entities = {}

    def collect_entities_after_flush(self, obj, status):
        if status in self.flush_interest:
            self.flush_entities.setdefault(status, set()).add(obj)
        if status in self.commit_interest:
            self.commit_entities.setdefault(status, set()).add(obj)

    def collect_entities_before_flush(self, obj, status):
        if status in self.pre_flush_interest:
            self.pre_flush_entities.setdefault(status, set()).add(obj)

    def after_flush_postexec(self):
        method = getattr(self, 'on_flush', None)
        if not method:
            return
        entities = []
        for status in self.flush_interest:
            '''
            阅后即焚，避免陷入flush->flush_postexec->flush死循环
            '''
            entities.append(self.flush_entities.pop(status, set()))
        method(*entities)

    def after_commit(self):
        method = getattr(self, 'on_commit', None)
        if not method:
            return
        entities = []
        for status in self.commit_interest:
            entities.append(self.commit_entities.pop(status, set()))
        method(*entities)

    def before_flush(self):
        method = getattr(self, 'pre_flush', None)
        if not method:
            return
        entities = []
        for status in self.pre_flush_interest:
            entities.append(self.pre_flush_entities.pop(status, set()))
        method(*entities)

    def before_commit(self):
        pass


class CommonEntityHook(EntityHook):

    def update_children_count(
            self, children, parent_name, children_name, counter_name, by_len=False):
        '''
        全量式更新统计表的count值，效率低，有一致性保证
        '''
        parents = set([])
        for child in children:
            parent = getattr(child, parent_name, None)
            if not parent:
                continue
            if parent and parent not in parents:
                if not by_len:
                    setattr(parent, counter_name,
                            getattr(parent, children_name)
                            .order_by(None).count())
                else:
                    setattr(parent, counter_name,
                            len(getattr(parent, children_name)
                                .all()))
                parents.add(parent)

    def increase_children_count(
            self, children, parent_name, counter_name, sign):
        '''
        增量式更新统计表的count值，效率高，缺乏一致性
        '''
        parents = {}
        for child in children:
            parent = getattr(child, parent_name, None)
            if not parent:
                continue
            parents[parent] = parents.get(parent, 0) + 1
        for parent, _count in parents.items():
            _cur_count = getattr(parent, counter_name, 0)
            if (_cur_count is None or _cur_count == 0) and sign > 0:
                # for insert
                setattr(parent, counter_name, _count)
            else:
                # for update
                setattr(
                    parent, counter_name,
                    getattr(parent.__class__, counter_name) + _count * sign)
