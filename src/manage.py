#!/usr/bin/env python
import os
COV = None
if os.environ.get('OJ_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='oj/*')
    COV.start()

from oj import app, db
from oj.models import UserModel
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, UserModel=UserModel)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

server_name = app.config['SERVER_NAME']
if server_name:
    uri = server_name.split(':')
    if len(uri) == 2:
        host, port = uri[0], uri[1]
    elif len(uri) == 1:
        host, port = uri[0], 80
    else:
        host, port = '0.0.0.0', '5000'
else:
    host, port = '0.0.0.0', '5000'
server = Server(host=host, port=port)
manager.add_command("runserver", server)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('OJ_COVERAGE'):
        import sys
        os.environ['OJ_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from oj.models import RoleModel

    # migrate database to latest revision
    upgrade()

    RoleModel.insert_roles()


if __name__ == '__main__':
    manager.run()
