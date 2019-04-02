# -*- coding: utf-8 -*-
import requests, os, time,chardet
from bs4 import BeautifulSoup
from urllib.parse import urljoin
class spider(object):
    def __init__(self,starturl,type = 'annoucement'):
        current_path = os.getcwd()
        parent_path = os.path.dirname(current_path)
        self.datapath = os.path.join(parent_path,'data',type)
        self.starturl = starturl
        if not os.path.exists(self.datapath):
            os.makedirs(self.datapath)

    def start_url(self, url = 'no url'):
        if url == 'no url':
            url = self.starturl
        r = requests.get(url)
        html = r.text
        next_page_url = self.parse(html)
        if next_page_url != None:
            time.sleep(5)
            self.start_url(next_page_url)

    def parse(self,html):
        soup = BeautifulSoup(html,'html.parser')
        art_url_a = soup.find_all('a',{'class': 'art_word'})
        for art_url in art_url_a:
            art_url = art_url['href']
            art_url = urljoin(self.starturl,art_url)
            self.get_content(art_url)

        next_page = soup.find('a',{'class' :'fr' })
        if next_page != None:
            next_page_url = next_page['href']
            next_page_url = urljoin(self.starturl,next_page_url)
        else:
            next_page_url = None
        return next_page_url

    def get_content(self,art_url):
        r = requests.get(art_url)
        html = r.content.decode('gbk').encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('span',{'id':'Ftitle'}).get_text()

        date = soup.find('span',{'id':'Freleasetime'}).get_text()
        pagedetail = soup.find('div',{'id':'pageDetail'}).get_text()
        filename = '{}{}.txt'.format(date[0:9],title)
        content = '{}\n{}\n{}'.format(title,date,pagedetail)

        self.savedata(filename,content)

        time.sleep(5)



    def savedata(self,filename, content):
        filepath = os.path.join(self.datapath,filename)
        if not os.path.exists(filepath):
            with open(filepath,'a+',encoding='utf-8') as f:
                f.write(content)
        print('success {}'.format(filename))


if __name__ == "__main__":
    url = 'http://pvp.qq.com/webplat/info/news_version3/15592/24091/24092/24095/m15240/list_1.shtml'
    sp =spider(starturl=url)
    sp.start_url()


