# -*- coding: utf-8 -*-
import scrapy
import os
from nculibtest.items import NculibtestItem as Items
from scrapy.http import Request


AimUrl = "http://210.35.251.243/newbook/newbook_cls_book.php" \
         "?back_days=15&loca_code=ALL&cls=ALL&s_doctype=ALL&clsname=%E5%85%A8%E9%83%A8%E6%96%B0%E4%B9%A6&page="


class NculibnewbookSpider(scrapy.Spider):
    name = 'nculibnewbook'
    allowed_domains = ['http://210.35.251.243/newbook/newbook_cls_browse.php']
    start_urls = [AimUrl + "1"]
    url_set = set()

    def parse(self, response):
        if response.url.startswith(AimUrl):
            books = response.xpath('//div[@class="list_books"]')
            for book in books:
                item = Items()
                item['name'] = book.xpath('.//a[@title="查看该书详细信息"]/text()').extract()[0]
                item['addr'] = book.xpath('.//a[@title="查看该书详细信息"]//@href').extract()[0]
                yield item
        urls = response.xpath('.//a[@class="blue"]//@href').extract()
        for url in urls:
            if response.url.startswith(AimUrl):
                # i = 0
                # if int(re.findall(r"(?<=page=)\d+", url)[0]) <= i:
                #     pass
                # else:
                #     i += 1
                #     yield self.make_requests_from_url("http://210.35.251.243/newbook/newbook_cls_book.php"+url)
                # 正则查找页数，不往前页查找
                if url in NculibnewbookSpider.url_set:
                    pass
                else:
                    NculibnewbookSpider.url_set.add(url)
                    yield self.make_requests_from_url("http://210.35.251.243/newbook/newbook_cls_book.php"+url)
            else:
                pass
