# -*- coding: utf-8 -*-
import scrapy
from nculibtest.items import NculibtestItem as Items

list_url = "http://210.35.251.243/browse/cls_browsing_book.php?s_doctype=all&cls="
tree_url = "http://210.35.251.243/browse/cls_browsing_tree.php?s_doctype=all&cls="
book_url = "http://210.35.251.243/opac/item.php?marc_no="


class NculibcrawlerSpider(scrapy.Spider):
    name = 'NcuLibCrawler'
    allowed_domains = ['210.35.251.243/browse/']
    start_urls = [tree_url + "&cls=A&lvl=1"]
    url_set = set()  # 存储已爬过的url
    custom_settings = {
        "cookie":   "PHPSESSID=jnk7r2vetq1cro9ml14fj88me6"
    }

    def parse(self, response):
        if response.url.startswith(list_url):  # 如果收到list url，爬取图书url，如果是最后一页，还yield下一个tree ch
            ch = response.url[69]
            title = response.xpath('//font[@color="red"]/text()').extract()[0]

            if len(title) > 3:
                books = response.xpath('//div[@class="list_books"]')  # 查找<div class="list_books">

                for book in books:
                    item = Items()
                    item['name'] = book.xpath('.//a[@title="查看该书详细信息"]/text()').extract()[0]
                    item['addr'] = book.xpath('.//a[@title="查看该书详细信息"]//@href').extract()[0][25:]
                    NculibcrawlerSpider.url_set.add(response.url)
                    yield item

                urls = response.xpath('.//a[@class="blue"]//@href').extract()  # 查找下一页url
                if "下一页" not in response.xpath('.//a[@class="blue"]/text()').extract():
                    if ch == 'K':
                        ch = 'M'
                    yield self.make_requests_from_url(tree_url + chr(ord(ch)+1) + "&lvl=1")
                else:
                    for url in urls:
                        if response.url.startswith(list_url):
                            if url in NculibcrawlerSpider.url_set:
                                pass
                            else:
                                NculibcrawlerSpider.url_set.add(url)
                                yield self.make_requests_from_url(
                                    "http://210.35.251.243" + url)
                        else:
                            pass

        elif response.url.startswith(tree_url):  # 如果收到tree url，爬取目录下中图法序号，并返回由序号决定的新list url
            cls = [x[4:] for x in response.xpath('//div[@class="stepright2"]/@name').extract()]
            for cl in cls:
                yield self.make_requests_from_url(list_url + cl)

        elif response.url.startswith(book_url):

