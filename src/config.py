# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = (
        os.environ.get('SECRET_KEY') or
        '\x11\xbe\xbb\xf0\x7fz\x9d\x01\x07\xa0'
        '\xd0J\xec\xbdw\nfc\xc5Q\xd0\x8cd\xf1')
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.163.com'
    # MAIL_SERVER = 'smtp.sina.cn'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    OJ_MAIL_SUBJECT_PREFIX = '[SDTU OJ]'
    OJ_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    OJ_ADMIN = os.environ.get('MAIL_USERNAME')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL')
        or 'postgresql+psycopg2://oj:oooo@localhost/oj')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('TEST_DATABASE_URL')
        or 'postgresql+psycopg2://oj:oooo@localhost/oj')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'postgresql+psycopg2://oj:oooo@localhost/oj')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.OJ_MAIL_SENDER,
            toaddrs=[cls.OJ_ADMIN],
            subject=cls.OJ_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


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
