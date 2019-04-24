import requests
from bs4 import BeautifulSoup


class dang_book:
    def __init__(self, isbn, book_name=''):
        data = self.dang_book_url(isbn, book_name)

        self.data = data
        self.book_url = data["title-url"]
        self.img_url = data["img-url"]

    def dang_book_url(self, isbn, book_name=''):

        url = 'http://search.dangdang.com/?key={}'.format(str(isbn).replace('-',''))

        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3766.2 Safari/537.36',
            'Upgrade - Insecure - Requests': '1',
        }
        res = requests.get(url, headers=header)
        data = {"title-url": "unknow",
                "img-url": "unknow"}

        if book_name in res.text:
            soup = BeautifulSoup(res.text, 'lxml')
            titles = soup.select('p.name > a')
            img_urls = soup.select('div > ul > li > a > img')

            title_url = titles[0].get('href')
            data["title-url"] = title_url

            for k, i in enumerate(img_urls):
                if book_name in str(i):
                    img_url = i.get('src').replace('_b_', '_w_')
                    data["img-url"] = img_url
                    break


            return data
        else:
            return data

    def dang_img(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3766.2 Safari/537.36',
        }
        res = requests.get(url, headers=header)

        soup = BeautifulSoup(res.text, 'lxml')
        book_img_url = soup.select('#largePic')
        # descrip = soup.select('content')
        # print(descrip)
        img_url = book_img_url[0].get('src')
        return img_url


url = dang_book(isbn='9787520312349', book_name='法律')
print(url.img_url)


# http://img3m6.ddimg.cn/9/29/1384799436-1_w_1.jpg w 是中等大小  u是超大图
