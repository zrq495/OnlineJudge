# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask.ext.admin import expose, expose_plugview
from flask import request, jsonify
from flask import views

from . import flask_admin
from .mixin import BaseViewMixin
from oj.core.logic import CkFinder


class FileManagerView(BaseViewMixin):

    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return self.render('admin/file_manager.html')

    @expose_plugview('/filemanager/')
    class GetInfoView(views.MethodView):

        def post(self, cls):
            ckfinder = CkFinder()
            upload_path = request.form.get('currentpath', '')
            new_file = request.files['newfile']
            return ckfinder.upload(upload_path, new_file)

        def get(self, cls):
            ckfinder = CkFinder()
            action = request.args.get('mode', '')
            if "getinfo" == action:
                info = ckfinder.get_info(request.args.get("path", ""))
                return jsonify(info)
            elif "getfolder" == action:
                return jsonify(ckfinder.get_dir_file(request.args.get("path", "")))
            elif "rename" == action:
                old_name = request.args.get("old", "")
                new_name = request.args.get("new", "")
                return ckfinder.rename(old_name, new_name)
            elif "delete" == action:
                path = request.args.get("path", "")
                return ckfinder.delete(path)
            elif "addfolder" == action:
                path = request.args.get("path", "")
                name = request.args.get("name", "")
                return ckfinder.addfolder(path, name)
            else:
                return "fail"

    @expose_plugview('/filemanager/dirlist/')
    class DirListView(views.MethodView):

        def post(self, cls):
            ckfinder = CkFinder()
            return ckfinder.dir_list(request)

flask_admin.add_view(FileManagerView(name='文件管理', url='filemanager'))
