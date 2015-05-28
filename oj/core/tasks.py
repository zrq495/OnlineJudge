# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import requests
from celery import Celery
from flask import render_template
from flask.ext.mail import Message

from oj import app, mail


def make_celery():
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery()


@celery.task()
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['OJ_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['OJ_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@celery.task()
def send_cloud_email(to, subject, template, **kwargs):
    url = "https://sendcloud.sohu.com/webapi/mail.send.json"
    params = {
        "api_user": app.config['SEND_CLOUD_API_USER'],
        "api_key": app.config['SEND_CLOUD_API_KEY'],
        "to": to,
        "from": app.config['OJ_MAIL_SENDER'],
        "fromname": 'SDUT Online Judge',
        "subject": app.config['OJ_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        "html": "你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！",
    }
    r = requests.post(url, files={}, data=params)
    print r
