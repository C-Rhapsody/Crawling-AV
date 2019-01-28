# -*- coding:utf-8 -*-

import requests
from lxml import html
import transmissionrpc
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import os


#################################################################################
# Define
urls = {
    "야동.노모": "https://bamenamja.com/bbs/board.php?bo_table=torrent01",
    "야동.유모": "https://bamenamja.com/bbs/board.php?bo_table=torrent02",
    "야동.한국": "https://bamenamja.com/bbs/board.php?bo_table=torrent03",
    "야동.서양": "https://bamenamja.com/bbs/board.php?bo_table=torrent04",
}

custom_useragent = str(UserAgent().chrome)


#################################################################################
# Transmission Config
tc_address = 'localhost'
tc_port_num = 9091
tc_user = None
tc_pass = None
tc = transmissionrpc.Client(
    address=tc_address, port=tc_port_num, user=tc_user, password=tc_pass
)

#################################################################################
# Action

def transmission(dir, seed_locate):
    try:
        # Transmission 데몬이 Local에서 동작할 때 정상동작
        tc.add_torrent('file:///' + seed_locate, download_dir="/downloads/complete/" + dir)
    except:
        return False

def child(dir, url):
    with requests.Session() as s:
        s.headers.update({'User-Agent' : custom_useragent})
        res = s.get(url)
        if not res.status_code == 200:
            return False
        content = html.fromstring(res.content)
        try:
            filename = content.xpath( \
                '/html/body/div[1]/div/div/div[5]/div/div/div[1]/div[1]/section/article/div[1]/div/a/text()[last()]' \
                )[0].strip().split('.torrent')[0] + '.torrent'
            link = content.xpath('/html/body/div[1]/div/div/div[5]/div/div/div[1]/div[1]/section/article/div[1]/div/a/@href')[0]
            res = s.get(link)
            with open(filename, 'wb') as file:
                file.write(res.content)
            transmission(dir, filename)
            os.remove(filename)
        except:
            return False


def main(dir, url):
    with requests.Session() as s:
        s.headers.update({'User-Agent' : custom_useragent})
        res = s.get(url)
        if not res.status_code == 200:
            print("Failed")
            return False
        content = html.fromstring(res.content)
        tables = content.xpath('//li[@class="list-item"]')
        for t in tables:
            title = t.xpath('./div[3]/a/text()')[1].strip()
            link = t.xpath('./div[3]/a/@href')[0]
            try:
                timestamp = t.xpath('./div[4]/span/text()')[0].strip()
            except:
                timestamp = t.xpath('./div[4]/text()')[0].strip()
            if timestamp >= (datetime.now() - timedelta(1)).strftime('%m.%d'):
                print(title, timestamp)
                child(dir, link)
            else:
                return False
        return True
                
if __name__ == "__main__":
    for key, url in urls.items():
        i = 0
        while True:
            i = i + 1
            if not main(key, url + '&page={}'.format(i)):
                break