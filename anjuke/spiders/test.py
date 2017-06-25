# -*- coding=utf-8 -*-


from scrapy import Spider
from scrapy import Request, FormRequest
from scrapy.selector import Selector
from encrypt import encrypted_request


class Fang(Spider):
    name = 'test'
    
    def __init__(self, *a, **kw):
        super(Fang, self).__init__(*a, **kw)
    
    def start_requests(self):
        param = {
            'page': 1,
            'area': 'EA',
        }
        
        data = encrypted_request(param)
        self.log('data:%s' % data)
        
        yield FormRequest(
            url = 'http://music.163.com/weapi/album/new?csrf_token=',
            formdata = data,
            headers = {
                'Host': 'music.163.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Referer': 'http://music.163.com/discover/album/',
            },
            callback = self.parse
        )
    
    def parse(self, response):
        self.log(response.body)
