import time
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Accept":"*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection":	"keep-alive",
  }


class Downloader:
    def __init__(self):
        self.soup = None
        self.brw =  requests.Session()
        self.brw.headers.update(HEADERS)
        
    def get_time(self):
        t = time.localtime(time.time())
        return '_'.join([str(i) for i in [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min]])
    
    def get_link(self, link, retries=0):
        r = self.brw
        r = r.get(link)
        if r.status_code == 200:
            self.soup = BeautifulSoup(r.text, 'html5lib')
            return r.text
        elif retries > 0 and r.status_code <500  and r.status_code > 400:
            return self.crawl(link,retries-1)
        else:
            return None

    def dowload(self, link, filetype=None, filename=None):
        pass

    
class Subreddit:
    def __init__(self, name):
        self.name = name
        self.page = 0
        self.next_page = ''

    def first_page(self):
        dwn = Downloader()
        raw_jsn = dwn.get_link('https://gateway.reddit.com/desktopapi/v1/subreddits/{}?rtj=debug&redditWebClient=web2x&app=web2x-client-production&dist=11&layout=card&sort=hot&allow_over18=1&include='.format(self.name))
        if raw_jsn:
            self.page = 1
            jsn = json.loads(raw_jsn)
            a_tmp = []
            for key in jsn['postIds']:
                item =jsn['posts'][key]
                tmp = {}
                tmp['numComments'] = item['numComments']
                tmp['author'] = item['author']
                tmp['score'] = item['score']
                tmp['created'] =item['created']
                tmp['title'] =item['title']
                tmp['id'] =item['id']
                tmp['authorId'] =item['authorId']
                tmp['permalink'] =item['permalink']
                if len(tmp['id'])<10:
                    a_tmp.append(tmp)
            df = pd.DataFrame(a_tmp, columns=['title', 'author', 'created', 'score', 'permalink','numComments','id','authorId'])
            self.next_page = 'https://gateway.reddit.com/desktopapi/v1/subreddits/gameofthrones?rtj=debug&redditWebClient=web2x&app=web2x-client-production&after={}&dist=11&layout=card&sort=hot&allow_over18=1&include='.format(self.name, jsn['token'])
            return df
        else:
            print('Unable to load the first page')
    


    