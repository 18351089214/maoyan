import requests
from bs4 import BeautifulSoup
import time
import random
from requests.packages import urllib3

urllib3.disable_warnings()


def get_page(offset):
    """
    :param offset: offset
    :return: html
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
    }

    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(e.args)
        return None


def parse_page(html):
    """
    :param html: html
    :return: item
    """
    soup = BeautifulSoup(html, 'lxml')
    for dd in soup.find_all(name='dd'):
        yield {
            'index': dd.i.string,
            'img': dd.find(name='img', attrs={'class': 'board-img'}).attrs['data-src'],
            'name': dd.find(name='a', attrs={'class': 'image-link'}).attrs['title'],
            'star': dd.find(name='p', attrs={'class': 'star'}).string.strip(),
            'releasetime': dd.find(name='p', attrs={'class': 'releasetime'}).string.split('：')[1],
            'score': dd.find(name='i', attrs={'class': 'integer'}).string + dd.find(name='i',
                                                                                    attrs={'class': 'fraction'}).string
        }


def main(offset):
    """
    :param offset: offset
    :return:
    """
    for item in parse_page(get_page(offset)):
        print(item)


if __name__ == '__main__':
    for offset in range(1, 11):
        st = random.random()
        print('休眠时间： ', st)
        time.sleep(st)
        main(offset * 10)
