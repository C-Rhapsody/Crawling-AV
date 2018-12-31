#-*- coding: utf-8 -*-

##############################################################################
# Import Modules
import requests
from lxml import html
from fake_useragent import UserAgent
import re
import transmissionrpc

##############################################################################
# Match Keyword
jav = re.compile('fc.*ppv|fc2|carib|1pon|sky|10mu|heyzo|[(]hey[)]|ssdv|smbd|一本道|rhj|red hot jam|xxx-av|加勒比')
unc = re.compile('金髪天國|金髪天国|金8天国|金8天國|kin8')

##############################################################################
# URL & Browser
base_url = 'https://sukebei.nyaa.si'
search_url = base_url + '/?c=2_2&p='
ua = UserAgent()
custom_useragent = str(ua.chrome)

##############################################################################
# Transmission Daemon
tc_address = 'localhost'
tc_port_num = 9091
tc_user = None
tc_pass = None
tc = transmissionrpc.Client(
    address=tc_address, port=tc_port_num, user=tc_user, password=tc_pass
)


##############################################################################
# Action
def download(dir, seed_locate):
    try:
        print(seed_locate)
        tc.add_torrent(seed_locate, download_dir="/downloads/complete/" + dir)
    except:
        return False

def main(search_url):
    with requests.session() as s:
        s.headers.update({'User-Agent': custom_useragent})
        url = search_url + str(1)
        res = s.get(url)
        if not res.status_code == 200:
            return False
        content = html.fromstring(res.content)
        tables = content.xpath('/html/body/div/div[2]/table/tbody/tr')
        for table in tables:
            title = table.xpath('./td[2]/a[last()]')
            res = s.get(base_url + title[0].attrib['href'])
            if not res.status_code == 200:
                return False
            content = html.fromstring(res.content)
            link = content.xpath('/html/body/div/div[2]/div[3]/a[1]/@href')
            if jav.search(title[0].text.lower()): download('야동.노모', base_url + link[0])
            if unc.search(title[0].text.lower()): download('야동.서양', base_url + link[0])
            #if jav.search(title[0].text.lower()): print('야동.노모', title[0].text)
            #if unc.search(title[0].text.lower()): print('야동.서양', title[0].text)

if __name__ == "__main__":
    main(search_url)
