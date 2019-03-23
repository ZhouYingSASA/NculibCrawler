# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NculibtestPipeline(object):
    def process_item(self, item, spider):
        with open(r"./list.txt", 'a') as fp:
            fp.write(str(item['name']) + '\n' + str(item['addr']) + '\n\n')
