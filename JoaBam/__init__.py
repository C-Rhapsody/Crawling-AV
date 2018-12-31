#-*- coding: utf-8 -*-

##############################################################################
# Import Modules
import requests
from lxml import html
from fake_useragent import UserAgent
from datetime import date, timedelta
import transmissionrpc
import progressbar
import os

##############################################################################
# URL & Browser
list_url = {
    '야동.한국': 'https://joabam.com/bbs/board.php?bo_table=torkor',
    '야동.서양': 'https://joabam.com/bbs/board.php?bo_table=torwest',
    '야동.노모': 'https://joabam.com/bbs/board.php?bo_table=torjpnno',
    '야동.유모': 'https://joabam.com/bbs/board.php?bo_table=torjpnyu',
}
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
def transmission(dir, seed_locate):
    try:
        # Transmission 데몬이 Local에서 동작할 때 정상동작
        tc.add_torrent('file:///' + seed_locate, download_dir="/downloads/complete/" + dir)
    except:
        return False

def download(dir, url):
    with requests.session() as s:
        s.headers.update({'User-Agent': custom_useragent})
        res = s.get(url)
        if not res.status_code == 200:
            return False
        content = html.fromstring(res.content)
        title = content.xpath('//h1/@content')[0]
        seed_locate = content.xpath('//a[@class="list-group-item break-word view_file_download at-tip"]/@href')[0]
        seed_name = content.xpath('//a[@class="list-group-item break-word view_file_download at-tip"]/text()')[0].strip().split('.torrent')[0] + '.torrent'
        print(title)
        res = s.get(seed_locate, stream=True)
        file_size = int(res.headers['Content-Length'])
        chunk = 1
        num_bars = file_size / chunk
        bar =  progressbar.ProgressBar(maxval=num_bars).start()
        with open(seed_name, 'wb') as f:
            i = 0
            for chunk in res.iter_content():
                f.write(chunk)
                bar.update(i)
                i+=1
        print(os.path.realpath(seed_name) + '\r\n')
        transmission(dir, os.path.realpath(seed_name))
        os.remove(os.path.realpath(seed_name))

def main(dir, url):
    with requests.session() as s:
        s.headers.update({'User-Agent': custom_useragent})
        index = 0
        while True:
            index = index + 1
            req = s.get(url + '&page=' + str(index))
            if not req.status_code == 200:
                return False
            content = html.fromstring(req.content)
            tables = content.xpath('//div[@class="img-item"]')
            for table in tables:
                if (date.today() - timedelta(1)).strftime('%m.%d') == \
                table.xpath('../../../div/span[@class="pull-left"]/text()')[0].replace('\r\n','').replace('\t',''):
                    download(dir, table.xpath('./a/@href')[0])
                else:
                    return 

if __name__ == "__main__":
    for key, url in list_url.items():
        main(key, url) 