import requests
from pyquery import PyQuery as pq
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
    doc = pq(html)
    for dd in doc('dl.board-wrapper dd').items():
        yield {
            'index': dd('dd > i').text(),
            'img': dd('img.board-img').attr['data-src'],
            'name': dd('dd a.image-link').attr('title'),
            'star': dd('p.star').text(),
            'releasetime': dd('p.releasetime').text(),
            'score': dd('i.integer').text() + dd('i.fraction').text(),
        }


def main(offset):
    """
    :param offset: offset
    :return:
    """
    for item in parse_page(get_page(offset)):
        print(item)


if __name__ == '__main__':
    for offset in range(0, 11):
        st = random.random()
        print('休眠时间： ', st)
        time.sleep(st)
        main(offset * 10)
