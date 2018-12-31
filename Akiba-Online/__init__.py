#-*- coding:utf-8 -*-

##############################################
# import module

from os import path, sys
import requests
from lxml import html
from datetime import datetime, timedelta
from time import mktime, strptime, sleep
from fake_useragent import UserAgent
import transmissionrpc

##############################################
# Global Var

## 실행 기준 1일 이전 DateTimeValue 설정
cut_datetime = mktime((datetime.utcnow() - timedelta(days=1)).timetuple())

## url 모음
main_url = 'https://www.akiba-online.com/'
urls = {
  "야동.유모":"https://www.akiba-online.com/forums/jav-torrents.175/", 
  "야동.노모":"https://www.akiba-online.com/forums/jav-torrents.176/"
}

## Fake Useragent define
ua = UserAgent()
ua = {'User-Agent':str(ua.chrome)}

## Transmission define
down_path = '/downloads/complete/'
tc_address = 'localhost'
tc_port_num = 9000
tc_user = ''
tc_pass = ''
tc = transmissionrpc.Client(
  address=tc_address, port=tc_port_num, user=tc_user, password=tc_pass
)

## Black_list
Black_lists = [
    'pacopacomama',
    'c0930',
    'h4610',
    'h0930',
    'Heydouga',
    'GirlsDelta',
]

##############################################
# Black list Query
def Black_Query(values):
    for b in Black_lists:
        if not values.lower().find(b.lower()) == -1:
            return True

##############################################
# Main Page -> Child Page
def parent_page(key, url):
    page_num = 0
    while True:
        page_num = page_num + 1
        url = url + 'page-' + str(page_num)
        with requests.session() as s:
            page = s.get(url, headers = ua)
            if not page.status_code == 200:
                return False
            contents = html.fromstring(page.text)
            titles = contents.xpath('''
                //li[@class="discussionListItem withInnerBlock visible  "]
                /div[@class="innerBlock"]/div[@class="listBlock main"]/div/h3/a''')
            for title in titles:
                try:
                    reg_datetime = int(title.xpath('''
                        ../../../../div[@class='listBlock lastPost']/dl/dd/a/abbr/@data-time''')[0]
                        )
                    if(cut_datetime < reg_datetime):
                        Child_page(key, main_url + title.attrib['href'])
                except:
                    break

##############################################
# Child Page -> Add Transmission -> Finished
def Child_page(dir, url):
    with requests.session() as s:
        page = s.get(url, headers = ua)
        if not page.status_code == 200:
            return False
        contents = html.fromstring(page.text)
        attach_links = contents.xpath('''
            //li[@class="attachment"]/div/div[2]/h6[@class="filename"]/a''')
        for a in attach_links:
            try:
                reg_datatime = int(a.xpath('''
                    ../../../../../../../../div[@class="messageMeta ToggleTriggerAnchor"]/div[1]/span/a/abbr/@data-time
                ''')[0])
                if (reg_datatime > cut_datetime) and (a.text.lower().find('.torrent')):
                    if not Black_Query(a.text): # black list keywords pass
                        # tc add_torrent
                        tc.add_torrent(main_url + a.attrib['href'], download_dir=down_path + dir)
                        print('done')
            except:
                continue

##############################################
if __name__ == '__main__':
    for key, url in urls.items():
        parent_page(key, url)
