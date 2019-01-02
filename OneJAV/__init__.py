#-*- coding:utf-8 -*-

from os import system

from lxml import html
import transmissionrpc
import time
from datetime import date, timedelta
from fake_useragent import UserAgent
import requests

yesterday = date.today() - timedelta(1)
main_url = 'https://onejav.com'
list_urls = [
  main_url + yesterday.strftime('/%Y/%m/%d'),
  #'https://onejav.com/actress/%E6%B5%85%E7%94%B0%E7%B5%90%E6%A2%A8',
  #'https://onejav.com/actress/%E7%9C%9F%E7%99%BD%E6%84%9B%E6%A2%A8',
  #'https://onejav.com/actress/%E3%81%82%E3%81%9A%E5%B8%8C',
  #'https://onejav.com/actress/Rena%20Aoi',
  #'https://onejav.com/actress/%E5%A4%A9%E9%9F%B3%E3%81%82%E3%82%8A%E3%81%99',
  #'https://onejav.com/actress/%E6%B5%85%E9%87%8E%E3%81%88%E3%81%BF',
  #'https://onejav.com/actress/%E9%99%BD%E6%9C%A8%E3%81%8B%E3%82%8C%E3%82%93',
  #'https://onejav.com/actress/Nagomi',
  #'https://onejav.com/actress/%E3%81%82%E3%82%86%E3%81%AA%E8%99%B9%E6%81%8B',
  #'https://onejav.com/actress/Rin%20Hatsumi',
  #'https://onejav.com/actress/Nori%20Kawanami',
  #'https://onejav.com/actress/Aya%20Sasami',
  #'https://onejav.com/actress/Ai%20Hoshina',
  #'https://onejav.com/actress/%E9%80%A2%E5%92%B2%E3%82%86%E3%81%82',
  #'https://onejav.com/actress/Koharu%20Suzuki',
  #'https://onejav.com/actress/Yuna%20Ogura',
  #'https://onejav.com/actress/%E9%AB%98%E6%9D%89%E9%BA%BB%E9%87%8C',
  #'https://onejav.com/actress/%E6%9C%88%E5%B3%B6%E3%82%A2%E3%83%B3%E3%83%8A',
  #'https://onejav.com/actress/Mikako%20Abe',
  #'https://onejav.com/actress/Nozomi%20Arimura',
  #'https://onejav.com/actress/Ai%20Hoshina',
  #'https://onejav.com/actress/%E5%9D%82%E5%92%B2%E3%81%BF%E3%81%BB',
  #'https://onejav.com/actress/Tsubomi',
  #'https://onejav.com/actress/karen',
  #'https://onejav.com/actress/Mai%20Kaede',
  #'https://onejav.com/actress/%E3%82%B8%E3%82%A7%E3%83%9E',
  #'https://onejav.com/actress/Seiran%20Igarashi',
  #'https://onejav.com/actress/%E7%80%AC%E5%90%8D%E3%81%8D%E3%82%89%E3%82%8A',
  #'https://onejav.com/actress/Miyu%20Amano',
  #'https://onejav.com/tag/Sport',
  #'https://onejav.com/actress/%E6%AD%A6%E8%97%A4%E3%81%A4%E3%81%90%E3%81%BF',
  #'https://onejav.com/actress/Minami%20Hatsukawa',
  #'https://onejav.com/actress/Minami%20Aizawa',
  #'https://onejav.com/actress/%E6%A0%97%E8%A1%A3%E3%81%BF%E3%81%84',
  #'https://onejav.com/actress/%E6%9C%89%E8%8A%B1%E3%82%82%E3%81%88',
  #'https://onejav.com/actress/Moe%20Amatsuka',
  #'https://onejav.com/actress/Hikari%20Nagisa',
  #'https://onejav.com/actress/Sora%20Shiina',
  #'https://onejav.com/actress/%E6%A0%97%E8%A1%A3%E3%81%BF%E3%81%84',
  #'https://onejav.com/actress/%E6%A9%98%E8%8A%B9%E9%82%A3',
  #'https://onejav.com/actress/%E7%99%BD%E7%80%AC%E3%81%AA%E3%81%AA%E3%81%BF',
  #'https://onejav.com/actress/RION',
  #'https://onejav.com/actress/NIMO',
  #'https://onejav.com/actress/%E4%BD%B3%E8%8B%97%E3%82%8B%E3%81%8B',
  #'https://onejav.com/actress/Maria%20Aizawa',
  #'https://onejav.com/actress/Koko%20Masshiro',
  #'https://onejav.com/actress/%E6%B8%85%E6%9C%AC%E7%8E%B2%E5%A5%88',
  #'https://onejav.com/actress/%E9%80%A2%E6%B2%A2%E3%82%8A%E3%81%84%E3%81%AA',
  #'https://onejav.com/actress/%E7%80%AC%E5%90%8D%E3%81%8D%E3%82%89%E3%82%8A',
  #'https://onejav.com/actress/%E6%A1%83%E5%B0%BB%E3%81%8B%E3%81%AE%E3%82%93',
  #'https://onejav.com/actress/%E4%B8%AD%E6%9D%91%E7%9F%A5%E6%81%B5',
  #'https://onejav.com/actress/Suzu%20Honjou',
  #'https://onejav.com/actress/%E3%81%AA%E3%81%A4%E3%82%81%E6%84%9B%E8%8E%89',
]

# popular link append Sunday
if date.today().weekday() == 6:
    list_urls.append('https://onejav.com/popular/')

request_url = '?page='

black_lists = [
    'Sex Conversion',
    'Cross Dressing',
    'Mature Woman',
    'BBW',
    'Transsexual',
]

#black_actor = [
#
#]

###############################################################################
# Fake UserAgent
ua = UserAgent()
ua = {'User-Agent' : str(ua.chrome)}

###############################################################################
# Transmission - Localhost // Port 9000 <Default 9091> // User = None // Password = None
down_path = '/downloads/complete/야동.유모'
tc_address = 'localhost'
tc_port_num = 9091
tc_user = None
tc_pass = None
tc = transmissionrpc.Client(
  address=tc_address, port=tc_port_num, user=tc_user, password=tc_pass
)


###############################################################################
# Search Black List
def Search_Black(lists):
    for list in lists:
        for black_list in black_lists:
            if not list.text.strip().find(black_list) == -1:
                return True


if __name__ == "__main__":
    for url in list_urls:
        page_num = 0
        while True:
            with requests.session() as s:
                page_num += 1
                page = s.get(url + request_url + str(page_num), headers = ua)
                if page.status_code == 200:
                    print(url + request_url + str(page_num))
                    content = html.fromstring(page.content)
                    links = content.xpath('//a[@class="button is-primary is-fullwidth"]')
                    for link in links:
                        seed_locate = main_url + link.attrib['href']
                        try:
                            tags = link.xpath('../div[@class="tags"]/a[@class="tag is-light"]')
                            if not Search_Black(tags):
                                print('  ' + main_url + link.attrib['href'])
                                tc.add_torrent(seed_locate, download_dir=down_path)
                        except:
                            print('  ' + main_url + link.attrib['href'])
                            seed_locate = main_url + link.attrib['href']
                            tc.add_torrent(seed_locate, download_dir=down_path)
                else:
                    break
                time.sleep(0.3)

