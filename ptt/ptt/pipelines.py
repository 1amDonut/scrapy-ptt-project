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
            print(item['title'])
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

            print("文章名稱插入錯誤")
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

        #    print('content')
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
            print("num=", num[0])
            self.conn.commit()
        except pymysql.Error:

            print("文章回覆插入錯誤")
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
            print("num=",num[0])
        #    for row in item['comments']:
        #        print("num",num[0])
        #        print(row['reply'])
        #        self.cursor.execute(
        #            "INSERT INTO ptt_reply(article_id,nrec,reply,reply_date)"
        #            "VALUES(%s,%s,%s,%s)",
        #            (
        #                num[0],
        #                row['nrec'],
        #                row['reply'],
        #                row['reply_date'],
        #            )
        #        )
        #    print("============")
#
            self.conn.commit()
        except pymysql.Error:

            print("文章內文插入錯誤")
        return item
class MySQLPipeline:
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME','ptt')
        host = spider.settings.get('MYSQL_HOST','localhost')
        port = spider.settings.get('MYSQL_PORT',3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '')
        self.db_conn=MySQLdb.connect(host=host,port=port,db=db,
                                     user=user,passwd=passwd,charset='utf8')
        self.db_cur=self.db_conn.cursor()

    def close_spider(self,spider):
        self.db_conn.commit()
        self.db_conn.close()
    def process_item(self,item,spider):
        self.insert_db(item)
        return item
    def insert_db(self,item):
        sql = "insert into ptt_articles (article_title,article_date,article_ahref) values(%s, %s, %s)"
        values = (
            item["title"],
            item["date"],
            item["url"],
        )
        self.db_cur.execute(sql, values)

        #count_sql = "SELECT count(*)  FROM ptt_articles"
        #self.db_cur.execute(count_sql)
        #num = self.db_cur.fetchone()
        #print(num,num[0])

        num_sql = "SELECT article_id FROM ptt_articles where article_ahref = %s"
        values = (item["url"],)
        self.db_cur.execute(num_sql,values)
        num = self.db_cur.fetchone()

        insert_content_sql = "insert into ptt_content (article_id,store,product,content) values(%s, %s, %s, " \
                             "%s) "
        values = (
            num[0],
            item["store"],
            item["product"],
            item["content"],
        )
        self.db_cur.execute(insert_content_sql, values)

        for row in item['comments']:
            reply_sql = "insert into ptt_reply(article_id,nrec,reply,reply_date)values(%s, %s, %s, %s)"

            values = (
                num[0],
                row["nrec"],
                row["reply"],
                row["reply_date"],
            )
            self.db_cur.execute(reply_sql,values)

        return item