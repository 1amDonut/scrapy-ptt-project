# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import pymysql

class PttPipeline(object):
    def process_item(self, item, spider):
        return item
class DBPipeline(object ):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='', db='ptt', charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "INSERT INTO ptt_articles( article_title,article_date,article_ahref) "
                "VALUES(%s ,%s, %s)",
                (
                    item["title"],
                    item['date'],
                    item['url'],
                )
            )
            self.conn.commit()
        except pymysql.Error:

            print("插入錯誤")
        return item
class DBPipeline2(object ):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='', db='ptt', charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        try:

            # 取得資料庫總比數，作為ID
            self.cursor.execute("SELECT count(*) FROM `ptt_articles`")
            num = self.cursor.fetchone()

            self.cursor.execute(
                "INSERT INTO ptt_content(article_id,store,product,content)"
                "VALUES(%s,%s,%s,%s)",
                (
                    num[0],
                    item['store'],
                    item['product'],
                    item['content'],
                )
            )
            self.conn.commit()
        except pymysql.Error:

            print("插入錯誤")
        return item

class DBPipeline3(object ):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='', db='ptt', charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        try:

            # 取得資料庫總比數，作為ID
            self.cursor.execute("SELECT count(*) FROM `ptt_articles`")
            num = self.cursor.fetchone()

            for row in item['comments']:
                print("num",num[0])
                print(row['reply'])
                self.cursor.execute(
                    "INSERT INTO ptt_reply(article_id,nrec,reply,reply_date)"
                    "VALUES(%s,%s,%s,%s)",
                    (
                        num[0],
                        row['nrec'],
                        row['reply'],
                        row['reply_date'],
                    )
                )
            print("============")

            self.conn.commit()
        except pymysql.Error:

            print("插入錯誤")
        return item