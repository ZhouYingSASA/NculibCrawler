# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
import pymysql


class NculibtestPipeline(object):

    def __init__(self):
        from nculibtest.cache import cache_tool
        self.cache = cache_tool

    def process_item(self, item, spider):
        # 将URL存入缓存
        self.cache.insert("to_crawl", item['addr'])

        with open(r"./list.txt", 'a') as fp:
            fp.write(str(item['name']) + '\n' + str(item['addr']) + '\n\n')


class MySQLPipeline(object):

    def __init__(self):
        dbparams = {
            'host': '222.204.6.27',
            'user': 'root',
            'password': 'ncuhome@dev',
            'database': 'nculib',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self.sql = "insert into books (name, lib_id) values (%s, %s)"
        self.sql2 = "insert into books ()"

    def process_item(self, item, spider):
        if spider.name == "NcuLibCrawler":
            try:
                self.cursor.execute(self.sql, (item['name'], item['addr']))
                self.conn.commit()
            except pymysql.err.IntegrityError as e:
                print("INTEGRITY_ERROR____", e)
            return item
        elif spider.name == "book_spider":
            for i in ('个人责任者', 'press', 'category'):
                id = tb.execute("select author_id from authors where name = %s", (item[i]))
                if id:
                    item[i + "_id"] = id
                else:
                    tb.execute("insert into authors (name) values (%s)", (item[i]))
                    item[i + "id"] = tb.execute("select author_id from authors where name = %s", (item['author']))

            tb.execute("insert into books (name, author_id, press_id, total_page, price, ISBN,\
                       summary, lib_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (item["题名"], item["author_id"], item["press_id"], item["total_page"],
                        item["price"], item["ISBN"], item["summary"], item["lib_id"]))
            self.cursor.execute()

    def _conditional_insert(self, tb, item):
        self.cursor.execute(self.sql, (item["name"], item["addr"]))
        log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
