import requests
from bs4 import BeautifulSoup


def book_img(isbn, book_name: str = '') -> dict:

    data = {
        "img-url": "unknown",
    }

    url = 'https://www.amazon.cn/s?k={}'.format(str(isbn).replace('-', ''))
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3766.2 Safari/537.36',
    }
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'lxml')
    img_urls = soup.select('div > span > a > div > img')
    print(img_urls)
    for k, i in enumerate(img_urls):
        if book_name.lower() in str(i).lower():
            img_url = i.get('src').replace('_b_', '_w_')
            data["img-url"] = img_url
            break

    return data


book_img(9787302525806, 'python')
