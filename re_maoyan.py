import requests
import re
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
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?<div.*?board-item-main.*?class="name".*?">(.*?)</a></p>.*?class="star">(.*?)</p>.*?"releasetime">(.*?)</p>'
        '.*?"score".*?"integer">(.*?)</i>.*?"fraction">(.*?)</i></p>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'img': item[1],
            'name': item[2],
            'star': item[3].strip(),
            'releasetime': item[4].split("：")[1],
            'score': item[5] + item[6]
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
