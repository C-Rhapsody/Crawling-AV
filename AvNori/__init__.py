#-*- coding:utf-8 -*-

##############################################################################
# Import Modules
from lxml import html
import transmissionrpc
from datetime import date, timedelta
from fake_useragent import UserAgent
import requests

##############################################################################
# URL & Browser
urls = {
    '야동.노모': 'https://avnori.pro/bbs/board.php?bo_table=torrent_nmav',
    '야동.유모': 'https://avnori.pro/bbs/board.php?bo_table=torrent_ymav',
    '야동.서양': 'https://avnori.pro/bbs/board.php?bo_table=torrent_amav',
}
ua = UserAgent()
custom_useragent = str(ua.chrome)



##############################################################################
# Action
def Transmission(dir,url):
    print(url)

def Main(dir,url):
    with requests.session() as s:
        s.headers.update({'User-Agent': custom_useragent})
        res = s.get(url)
        if not res.status_code == 200:
            return False
        content = html.fromstring(res.content)
        tables = content.xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[3]/div/div')
        for t in tables:
            title = t.xpath('./div/div/h6/a/strong/text()')[0]
            link = t.xpath('./div/div/h6/a/@href')[0]
            reg_clock = t.xpath('./div/div/ul/li[2]/text()')[0].strip()
            if reg_clock == '오늘':
                res = s.get(link)
                if not res.status_code == 200:
                    return False
                content = html.fromstring(res.content)
                magnet = content.xpath('//button[@class="btn btn-success btn-xs"]/@onclick')[0]
                print(dir, title)
                Transmission(dir, 'magnet:?xt=urn:btih:' + magnet.split("'")[1])
            else:
                return False

if __name__ == "__main__":
    for key, url in urls.items():
        index = 0
        while True:
            index = index + 1
            if not Main(key, url + '&page=' + str(index)):
                break