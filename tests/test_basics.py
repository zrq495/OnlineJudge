from flask import current_app
from flask.ext.testing import TestCase
from oj import app, db
from oj.config import config


class BasicsTestCase(TestCase):

    def create_app(self):
        app.config.update(config['testing'].__dict__)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
