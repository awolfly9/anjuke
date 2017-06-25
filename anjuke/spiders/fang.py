# -*- coding=utf-8 -*-


from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector


class Fang(Spider):
    name = 'fang'
    
    def __init__(self, *a, **kw):
        super(Fang, self).__init__(*a, **kw)
        self.city_url = kw.get('url')
        
        'https://lijiang.anjuke.com'
        self.city = self.city_url.split('.')[0]
        self.city = self.city[8:]
    
    'https://bj.fang.anjuke.com/loupan/all/p1/'
    
    def start_requests(self):
        for i in range(0, 20):
            url = 'https://%s.fang.anjuke.com/loupan/all/p%s/' % (self.city, i)
            yield Request(
                url = url,
                headers = {
                    'Host': 'bj.fang.anjuke.com',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'
                },
                meta = {
                    'city': self.city
                },
                callback = self.get_fang_info
            )
    
    def get_fang_info(self, response):
        with open('log/fang.html', 'w') as f:
            f.write(response.body)
            f.close()
