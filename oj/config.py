# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = (
        os.environ.get('SECRET_KEY') or
        '\x11\xbe\xbb\xf0\x7fz\x9d\x01\x07\xa0'
        '\xd0J\xec\xbdw\nfc\xc5Q\xd0\x8cd\xf1')

    SQLALCHEMY_RECORD_QUERIES = True
    # SQLALCHEMY_ECHO = True

    # email
    # MAIL_SERVER = 'smtp.163.com'
    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    OJ_MAIL_SUBJECT_PREFIX = '[SDTU OJ]'
    OJ_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    OJ_ADMIN = os.environ.get('OJ_ADMIN')

    # pagination
    PROBLEM_START_ID = 1000
    PROBLEMS_PER_PAGE = 100
    NEWS_PER_PAGE = 5
    SOLUTIONS_PER_PAGE = 5
    RANK_PER_PAGE = 5
    CONTESTS_PER_PAGE = 5

    BOOTSTRAP_SERVE_LOCAL = True

    DEFAULT_PASSWORD = 'oj123456'

    TEST_DATA_PATH = '/data/'

    # send cloud
    SEND_CLOUD_API_USER = os.environ.get('SEND_CLOUD_API_USER')
    SEND_CLOUD_API_KEY = os.environ.get('SEND_CLOUD_API_KEY')

    # redis
    REDIS_URL = 'redis://%s:%s/%s' % (
        os.environ.get('REDIS_HOST', 'localhost'),
        os.environ.get('REDIS_PORT', '6379'),
        os.environ.get('REDIS_DATABASE', '1'),
    )

    # celery
    CELERY_BROKER_URL = 'redis://%s:%s' % (
        os.environ.get('REDIS_HOST', 'localhost'),
        os.environ.get('REDIS_PORT', '6379'))

    # frequency limitation
    ENABLE_TIMELIMIT = True
    SUBMIT_TIMELIMIT = 2

    PROGRAM_LANGUAGE = {
        'gcc': 'gcc',
        'g++': 'g++',
        'java': 'java',
    }

    SOLUTION_RESULT = {
        1: 'ACCEPTED',
        8: 'PE',
        2: 'TIME_LIMIT',
        3: 'MEMORY_LIMIT',
        4: 'WRONG_ANSWER',
        5: 'RUNTIME_ERROR',
        6: 'OUTPUT_LIMIT',
        7: 'COMPILE_ERROR',
        11: 'SYSTEM_ERROR',
        0: 'WAITING',
        12: 'JUDGEING',
    }

    CELERYBEAT_SCHEDULE = {
        'test': {
            'task': 'oj.core.tasks.test',
            'schedule': crontab(minute='*/1'),
            'args': (1, 2, 3)
        },
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # SQLALCHEMY_ECHO = True

    SERVER_NAME = os.getenv('OJ_SERVER_NAME') or 'dev.sdutacm.org:5000'

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL')
        or 'postgresql+psycopg2://oj:oooo@localhost/oj')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('TEST_DATABASE_URL')
        or 'postgresql+psycopg2://oj_test:oooo@localhost/oj_test')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):

    SERVER_NAME = os.getenv('OJ_SERVER_NAME') or 'do.zrq495.com:5000'

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'postgresql+psycopg2://oj:oooo@localhost/oj')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        # import logging
        # from logging.handlers import SMTPHandler
        # credentials = None
        # secure = None
        # if getattr(cls, 'MAIL_USERNAME', None) is not None:
            # credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            # if getattr(cls, 'MAIL_USE_TLS', None):
                # secure = ()
        # mail_handler = SMTPHandler(
            # mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            # fromaddr=cls.OJ_MAIL_SENDER,
            # toaddrs=[cls.OJ_ADMIN],
            # subject=cls.OJ_MAIL_SUBJECT_PREFIX + ' Application Error',
            # credentials=credentials,
            # secure=secure)
        # mail_handler.setLevel(logging.ERROR)
        # app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
