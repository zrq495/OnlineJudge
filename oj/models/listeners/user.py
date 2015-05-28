
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from oj import app

from .. import UserModel, RoleModel
from ..hook import entity, CommonEntityHook


@entity(UserModel)
class UserHook(CommonEntityHook):

    flush_interest = ['new', 'deleted']

    def on_flush(self, new_users, deleted_users):
        users = new_users | deleted_users
        self.update_user_role(users)

    def update_user_role(self, users):
        for user in users:
            if user.role is None:
                if user.email == app.config['OJ_ADMIN']:
                    user.role = RoleModel.query.filter_by(
                        permissions=0xff).first()
                if user.role is None:
                    user.role = RoleModel.query.filter_by(default=True).first()
