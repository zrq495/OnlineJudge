# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests
from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from oj import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['OJ_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['OJ_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_cloud_email(to, subject, template, **kwargs):
    url = "https://sendcloud.sohu.com/webapi/mail.send.json"
    params = {
        "api_user": current_app.config['SEND_CLOUD_API_USER'],
        "api_key": current_app.config['SEND_CLOUD_API_KEY'],
        "to": to,
        "from": current_app.config['OJ_MAIL_SENDER'],
        "fromname": 'SDUT Online Judge',
        "subject": current_app.config['OJ_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        "html": "你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！",
    }
    r = requests.post(url, files={}, data=params)
    print r
