# -*- coding : utf-8 -*-

import requests
from lxml import html
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import transmissionrpc
import os

#################################################################################
# Define
urls = {
    '야동.유모': 'https://19egg.com/bbs/board.php?bo_table=qka37',
    '야동.노모': 'https://19egg.com/bbs/board.php?bo_table=qka38',
    '야동.서양': 'https://19egg.com/bbs/board.php?bo_table=qka39',
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
    with requests.session() as s:
        s.headers.update({'User-Agent' : custom_useragent})
        res = s.get(url)
        if not res.status_code == 200:
            return False
        content = html.fromstring(res.content)
        try:
            timestamp = content.xpath('/html/body/div[3]/div/article/section[1]/strong[2]/text()')[0]
            if not datetime.strptime(timestamp, '%y-%m-%d %H:%M').timestamp() >= (datetime.now() - timedelta(1)).timestamp():
                return False
            filename = content.xpath('/html/body/div[3]/div/article/section[2]/ul/li[2]/a/strong/text()')[0]
            link = content.xpath('/html/body/div[3]/div/article/section[2]/ul/li[2]/a/@href')[0]
            res = s.get(link, stream = True)
            with open(filename, 'wb') as f:
                f.write(res.content)
            if transmission(dir, os.path.realpath(filename)):
                os.remove(os.path.realpath(filename))
            return True
        except:
            return False

def main(dir, url):
    with requests.session() as s:
        s.headers.update({'User-Agent' : custom_useragent})
        res = s.get(url)
        if not res.status_code == 200:
            return False
        content = html.fromstring(res.content)
        tables = content.xpath('/html/body/div[3]/div/div[3]/form/ul/li')
        for t in tables:
            try:
                if t.xpath('./ul/li[1]/a/strong/text()')[0] == '공지':
                    continue
            except:
                title = t.xpath('./ul/li[2]/a[2]/text()')[0].strip()
                link = t.xpath('./ul/li[2]/a[2]/@href')[0]
                if not child(dir, link):
                    return False
        return True
                
if __name__ == "__main__":
    for key, url in urls.items():
        i = 0
        while True:
            i = i + 1
            if not main(key, url +'&page={}'.format(i)):
                break