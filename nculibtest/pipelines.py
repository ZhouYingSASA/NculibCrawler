# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NculibtestPipeline(object):

    def __init__(self):
        from nculibtest.cache import cache_tool
        self.cache = cache_tool

    def process_item(self, item, spider):
        # 将URL存入缓存
        self.cache.insert(item['addr'])

        with open(r"./list.txt", 'a') as fp:
            fp.write(str(item['name']) + '\n' + str(item['addr']) + '\n\n')
