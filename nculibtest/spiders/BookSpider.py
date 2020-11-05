# encoding=gbk
import scrapy
import re
import pymysql
from nculibtest.cache import cache_tool

base_url = "http://210.35.251.243/opac/item.php?marc_no="


class BookSpider(scrapy.Spider):
    name = "book_spider"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dbparams = {
            'host': '222.204.6.27',
            'user': 'root',
            'password': 'ncuhome@dev',
            'database': 'nculib',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self.id = 24214

    # start_urls = ["http://210.35.251.243/opac/item.php?marc_no=" + ]

    def start_requests(self):
        # return base_url + cache_tool.pop("to_crawl")
        # while not self.cursor.execute("SELECT lib_id FROM books WHERE book_id = %s", self.id):
        #     self.id += 1
        # else:
        #     return [scrapy.Request(
        #         "http://210.35.251.243/opac/item.php?marc_no=" +
        #         self.cursor.fetchone()[0],
        #         callback=self.parse)]
        return [scrapy.Request(base_url + '2b714f6f436d62424e47435449376f5a6a77474a35673d3d', callback=self.parse)]

    def parse(self, res):
        key = re.findall("marc_no=(.+)", res.url)[0]
        if "���鿯�������ڶ����л��ߴ�����" in res.body.decode():
            cache_tool.insert("no_use", key)
            return
        dls = res.xpath('//*[@id="item_detail"]/dl')[:-2]

        # parse dls
        result = {'id': self.id}
        for dl in dls:
            dt = dl.xpath("dt/node()")[0].extract()[:-1]
            print(dt + ":", end=' ')
            dds = dl.xpath("dd/node()").extract()
            dd = ''
            for d in dds:
                dd += re.sub(r'<.*?>', '', d)
                print(dd)

                if '����/������' in dt:
                    dt = dt.split('/')[0]
                    dd = dd.split('/')[0]
                    break

                if '������' in dt[-3:] and '��Ҫ' not in dt:
                    dt = '����'
                    r = re.compile(r'[^\u4e00-\u9fa5]')
                    dd = re.sub(r, ' ', dd)
                    dd = dd.split()[0].split(' ')[0]

                if '���淢����' in dt:
                    dt = '������'
                    sp = re.split(r'[:,]', dd)
                    dd = sp[1]
                    result['����ʱ��'] = sp[-1]

                if 'ISBN������' in dt:
                    dt = 'ISBN'
                    sp = dd.split("/")
                    dd = sp[0]
                    result['����'] = sp[-1].replace(' ', '')

                if '��ע' in dt and '��Ҫ��ժ' not in dt:
                    dd = dt + ': ' + dd + '\n'
                    dt = '��ע'
            if dt not in result:
                result[dt] = dd
            else:
                result[dt] += ',' + dd

        # ����������
        result['����'] = re.sub(r'[ *?��]', '', result['����'])

        # ժҪ����
        if '��Ҫ��ժ��ע' in result:
            if '��ע' not in result:
                result['��ע'] = result.pop('��Ҫ��ժ��ע')
            else:
                result['��ע'] = result.pop('��Ҫ��ժ��ע') + "\n" + result['��ע']

        # �������ֶ�
        for i in ('����', '����', '��ע', '������', 'ѧ������', '������̬��', '����'):
            if i not in result:
                result[i] = None

        print(result)
        # self.id += 1
        # yield self.make_requests_from_url(base_url)
