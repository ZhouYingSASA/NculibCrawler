import requests, re
from bs4 import BeautifulSoup


def book_img(isbn, book_name: str = '') -> dict:

    data = {
        "img-url": "unknow",
    }

    url = 'https://www.amazon.cn/s?k={}'.format(str(isbn).replace('-', ''))
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3766.2 Safari/537.36',
    }
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'lxml')
    book_url = soup.select('div.s-result-list.sg-row > div > div > div > div > div > div > div > div > span > a.a-link-normal')

    img_urls = soup.select('div > span > a > div > img')
    for k, i in enumerate(img_urls):
        if book_name.lower() in str(i).lower():
            img_url = i.get('src').replace('_b_', '_w_')
            book_url = 'https://www.amazon.cn' + book_url[k].get('href')
            data["book-url"] = book_url
            data["img-url"] = img_url
            break

    return data


def book_descrip(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3766.2 Safari/537.36',
    }
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('noscript > div')
    descrip = data[0].get_text()
    descrip = re.findall(r'(?<=内容介绍：).*?(?=作者)', descrip)
    if descrip != []:
        return descrip[0]
    else:
        return 'unknow'


# test
# a = book_img(9787302525806, 'python')
# print(a)
# b = book_descrip('https://www.amazon.cn/dp/B07P4DPX2M/')
# print(b)

