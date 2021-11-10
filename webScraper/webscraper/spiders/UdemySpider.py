
import json
import scrapy
from scrapy import Request

from ..items import UdemyItem



class UdemySpider(scrapy.Spider):
    name = "udemy"
    allowed_domains = [
        "udemy.com"
    ]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    
    def start_requests(self):
        yield Request(
            'https://www.udemy.com/api-2.0/courses?page_size=100' ,
            callback=self.parse_details,
            headers={
                ":authority": "www.udemy.com",
                ":method": "GET",
                ":path": "/api-2.0/courses",
                ":scheme": "https",
                "Accept": "application/json, text/plain, */*",
                "Authorization": "Basic S084SmNDUDVBU1NFR0hGQTV4WVpSRDJUbVowNUZDNUt5THFxM2tSYTplNEdQOE4yOEViOVZ5U1Y0UVNnakpwcmUxM0l5alNWaDMwdG1iYUpkOFRkTmhpcXozMVBvUE1POUlya0w5SlNmY2ZnV0d3bWtFMnJVcURUV3JEbUxKTUxKWEtmcFc1RHJLM2VCQThTbGRTMkJlRU5UZzk5V2hhZTRmOUJvY1BZcg==",
                "Content-Type": "application/json;charset=utf-8",
                'user_agent ': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

            })

    def parse_details(self , response):
        data = json.loads(response.text)
        data = data['results']
        courses  = []
        for i in data :
            item = UdemyItem()
            item['title'] = i.get('title')
            item['id'] = i.get('id')
            item['price'] = i.get('price')
            item['link'] = i.get('url')
            item['description'] = i.get('headline')
            item['instructors'] = [d.get('name') for d in i.get('visible_instructors')]
            item['source'] = 'udemy'
            yield item