# encoding=gbk
import json
import scrapy
import re
from nculibtest.cache import cache_tool

base_url = "http://210.35.251.243/opac/item.php?marc_no="



class BookSpider(scrapy.Spider):

    name = "book_spider"

    def start_requests(self):
        # return base_url + cache_tool.pop("to_crawl")
        return [scrapy.Request("http://210.35.251.243/opac/item.php?marc_no=4c4d79504d6870522f464e6a6f494b647845326532513d3d", callback=self.parse)]

    def parse(self, res):
        key = re.findall("marc_no=(.+)", res.url)[0]
        if "此书刊可能正在订购中或者处理中" in res.body:
            cache_tool.insert("no_use", key)
            return
        dls = res.xpath('//*[@id="item_detail"]/dl')[:-2]

        # parse dls
        result = {}
        for dl in dls:
            dt = dl.xpath("dt/node()")[0].extract()
            print dt
            dd = dl.xpath("dd/node()")[0].extract()

            result[dt] = dd
        cache_tool.get_connect().hset("data_result", key, json.dumps(result))
