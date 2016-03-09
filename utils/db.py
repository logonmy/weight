#!/usr/bin/env python3
# coding: utf-8

'''
@author: u9648u6653u52c7@gmail.com
@date: 2016-03-09
@description: sqlite3 简易工具类
'''

import os
import re
import sqlite3


class DB(object):

    def __init__(self, name, path='.'):
        self.conn = None
        self.cur = None
        self.path = os.path.normpath(os.path.join(path, name))
        if not os.path.isfile(self.path):
            print('The dataBase is not exsit!')
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        pass

    def connect(self):
        return sqlite3.connect(self.path)

    def close(self):
        self.cur.close()
        self.conn.close()
        pass

    def hasTable(self, name):
        self.cur.execute('select * from sqlite_master where name=?', (name,))
        return bool(self.cur.fetchone())

    '''
    @params should be a tuple
    '''
    def createTable(self, name, params):
        if self.hasTable(name):
            return print('This table is exsit!')
        sql = 'create table ' + name + re.sub(r'(?:\'|\")', '', str(params))
        self.cur.execute(sql)
        self.conn.commit()
        pass

    def dropTable(self, name):
        if not self.hasTable(name):
            return print('This table is not exsit!')
        self.cur.execute('drop table '+name)
        self.conn.commit()
        pass

    def select(self):
        pass

    '''
    @params should be a dict
    '''
    def insert(self, name, params):
        keys, values = [], []
        for k, v in params.items():
            keys.append(k)
            values.append(v)
        keys = tuple(keys)
        values = tuple(values)
        sql = 'insert into ' + name + re.sub(r'(?:\'|\")', '', str(keys)) + ' values' + str(values)
        self.cur.execute(sql)
        self.conn.commit()
        pass

    def update(self):
        pass

    def delete(self):
        pass

    pass


x = DB('ty.db')


'''
x.createTable('user', ('id integer primary key autoincrement',
                       'name varchar(20)',
                       'weight varchar(20)',
                       'datetime varchar(20)'
                    ))

x.dropTable('user')



x.insert('user',{
    'name': 'Brave',
    'weight': '70.0',
    'datetime': '1234567'
})

'''