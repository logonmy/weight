#!/usr/bin/env python3
# coding: utf-8

'''
@author: u9648u6653u52c7@gmail.com
@date: 2016-03-03
@description: QQ空间说说信息抓取
'''

import os, re
from datetime import datetime
from .qqlib import QQ
from utils.db import DB

class Qzone(QQ):

    def getCSRFToken(skey):
        str = skey
        hash = 5381
        for val in str:
            hash += (hash << 5) + ord(val)
        return hash & 0x7fffffff

    def __init__(self, user, pwd, datebase):
        self.db = datebase
        super(Qzone, self).__init__(user, pwd)
        self.createQzoneDB()
        self.createEmotionTable()

    def createQzoneDB(self):
        qzoneDB = DB(self.db)
        qzoneDB.close()

    def createEmotionTable(self):
        qzoneDB = DB(self.db)
        qzoneDB.createTable('emotion', (
                                        'id integer primary key autoincrement',
                                        'name varchar(20)',
                                        'weight varchar(20)',
                                        'datetime varchar(20)'
                    ))
        qzoneDB.close()

    def isLogin(self):
        if self.session.cookies.get('uin', -1) == -1:
            return False
        else:
            return True

    def login(self):
        super(Qzone, self).login()

    '''
    @return {tuple}
    '''
    def getUpdateTimestamp(self):

        name = str(self.user) + '.txt'
        cwd = os.path.dirname(__file__)
        path = os.path.normpath(os.path.join(cwd, name))
        timestamp = str(int(datetime.now().timestamp()))

        if not os.path.isfile(path):
            with open(path, 'w') as file:
                file.write(timestamp)
            return timestamp, 0
        else:
            with open(path, 'r+') as file:
                lastTimestamp = file.readline()
                file.truncate(0)
                file.seek(0)
                file.write(timestamp)
            return timestamp, lastTimestamp

    def updateEmotion(self):
        timestamp, lastTimestamp = self.getUpdateTimestamp()
        url = 'http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6'
        params = {
            'uin': self.user,
            'pos': 0,
            'num': 20,
            'g_tk': Qzone.getCSRFToken(self.session.cookies.get('skey')),
            'code_version': 1,
            'format': 'json'
        }
        total, msgList, content, createdTime = None, None, None, None
        qzoneDB = DB(self.db)
        while True:
            res = self.session.get(url, params=params)
            data = res.json()
            total = data['total']
            msgList = data['msglist']

            for all in msgList:
                content = all['content']; createdTime = all['created_time']
                if int(createdTime) < int(lastTimestamp):
                    return qzoneDB.close()
                if int(createdTime) < int(timestamp) and int(createdTime) > int(lastTimestamp) \
                        and re.match(r'^～?\d{2}\.?\d?$', content):
                    # print(content, '#', createdTime)
                    qzoneDB.insert('emotion', {
                        'name': str(self.user),
                        'weight': content,
                        'datetime': createdTime
                    })

            # when to break loop
            if total < params['num'] or total < params['pos'] + params['num']:
                return qzoneDB.close()

            params['pos'] = params['pos'] + params['num']

'''
q = Qzone(12345, '12345')

def task():
    if not q.isLogin():
        q.login()
    q.updateEmotion()
    print('hello python!')

# 定时任务
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
sched.add_job(task, 'cron', hour='10-11')
sched.start()
'''