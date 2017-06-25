# -*- coding=utf-8 -*-

from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector


class City(Spider):
    name = 'city'
    
    'https://www.anjuke.com/sy-city.html'
    def start_requests(self):
        url = 'https://www.anjuke.com/sy-city.html'
        yield Request(
            url = url,
            headers = {
                'Host': 'www.anjuke.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
            },
            callback = self.get_city
        )
    
    def get_city(self, response):
        with open('log/city.html', 'w') as f:
            f.write(response.body)
            f.close()
        
        sel = Selector(response)
        citys = sel.xpath('//div[@class="letter_city"]/ul/li/div').extract()
        for i, city in enumerate(citys):
            sel = Selector(text = city)
            city_name = sel.xpath('//a/text()').extract()
            city_url = sel.xpath('//a/@href').extract()
            
            for j, name in enumerate(city_name):
                self.log('city_name:%s city_url:%s' % (name, city_url[j]))
                
                url = city_url[j]
                yield Request(
                    url = city_url[j],
                    headers = {
                        'Host': '%s' % url[8:],
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 '
                                      'Firefox/54.0',
                    },
                    meta = {
                        'city': url[8:]
                    },
                    callback = self.get_city_page
                )
                
                # break
                
                # break
    
    def get_city_page(self, response):
        with open('log/%s.html' % response.meta.get('city'), 'w') as f:
            f.write(response.body)
            f.close()
        
        sel = Selector(response)
        fang_url = sel.xpath('//a[@class="a_navnew"]/@href').extract_first()
        self.log('fang_url:%s' % fang_url)
        'https://bj.fang.anjuke.com/'
        
        yield Request(
            url = fang_url,
            headers = {
                'Host': fang_url[8:-1],
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 '
                              'Firefox/54.0',
            },
            meta = {
                'city': response.meta.get('city'),
                'host': fang_url[8:-1],
                'page_count': 0
            },
            callback = self.get_fang_page
        )
    
    def get_fang_page(self, response):
        with open('log/%s_fang_%s.html' % (response.meta.get('city'), response.meta.get('page_count')), 'w') as f:
            f.write(response.body)
            f.close()
        
        sel = Selector(response)
        names = sel.xpath('//a[@class="items-name"]/text()').extract()
        for name in names:
            self.log('name:%s' % name)
        
        # 点击下一页，下一页是否存在
        next_page_url = sel.xpath('//a[@class="next-page next-link"]/@href').extract_first()
        if next_page_url != None:
            yield Request(
                url = next_page_url,
                headers = {
                    'Host': response.meta.get('host'),
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 '
                                  'Firefox/54.0',
                },
                meta = {
                    'city': response.meta.get('city'),
                    'host': response.meta.get('host'),
                    'page_count': int(response.meta.get('page_count')) + 1
                },
                callback = self.get_fang_page
            )
