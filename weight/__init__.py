#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@author: u9648u6653u52c7@gmail.com
@date: 2016-03-10
@description: flask
'''

import os
from utils.db import DB
from qzone import Qzone
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_apscheduler import APScheduler

app = Flask(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'qzone.sqlite'),
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:task',
            'trigger': 'cron',
            'hour': '10-11'
        }
    ],

    SCHEDULER_VIEWS_ENABLED = True
))


def task():
    q = Qzone(850105909, '*********', app.config['DATABASE'])
    if not q.isLogin():
        q.login()
    q.updateEmotion()
    pass


def createDateBase():
    db = DB(app.config['DATABASE'])
    db.close()

createDateBase()

@app.route('/')
def index():
    return 'The first python app.'

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
