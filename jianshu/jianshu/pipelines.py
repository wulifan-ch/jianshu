# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

class JianshuPipeline(object):
    def __init__(self):
        dbparams={
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu1',
            'charset': 'utf8'
        }
        self.con = pymysql.connect(**dbparams)
        self.cursor = self.con.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'], item['author'],
                                       item['image'], item['origin_url'], item['article_id']))
        self.con.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into article(id, title, content, author, image, origin_url, article_id) 
            values (null , %s, %s, %s, %s, %s, %s)
            '''
            return self._sql
        return self._sql

class JianShuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu1',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
                insert into article(id, title, content, author, image, origin_url, 
                article_id, like_count, subjects) 
                values (null , %s, %s, %s, %s, %s, %s, %s, %s)
                '''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['content'], item['author'],
                                  item['image'], item['origin_url'], item['article_id'],
                                  item['like_count'], item['subjects']))

    def handle_error(self, error, item, spider):
        print('='*10+'ERROR'+'='*10)
        print(error)
        print('='*10+'ERROR'+'='*10)
