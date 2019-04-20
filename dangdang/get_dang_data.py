import requests
from bs4 import BeautifulSoup



def dang_book_url(isbn,book_name=''):

    url = 'http://search.dangdang.com/?key={}act=input'.format(str(isbn))

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3766.2 Safari/537.36',
    }
    res = requests.get(url, headers=header)

    if book_name in res.text:
        soup = BeautifulSoup(res.text, 'lxml')
        titles = soup.select('p.name > a')
        title_url = titles[0].get('href')
        print(title_url)
        return title_url
    else:
        return None


def dang_data(url):

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3766.2 Safari/537.36',
    }
    res = requests.get(url, headers=header)

    soup = BeautifulSoup(res.text, 'lxml')
    book_img_url = soup.select('#largePic')
    # descrip = soup.select('content')
    # print(descrip)
    img_url = book_img_url[0].get('src')
    return img_url

dang_data('http://product.dangdang.com/1403535389.html')




