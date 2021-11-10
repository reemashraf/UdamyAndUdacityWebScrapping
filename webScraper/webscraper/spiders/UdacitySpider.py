
import json
import scrapy
from scrapy import Request
from scrapy.http import Response
from ..items import UdacityItem



class Udacity(scrapy.Spider):
    name = "udacity"
    allowed_domains = "*"
    start_url = "https://catalog-api.udacity.com/v1/courses"


    def start_requests(self):
        yield Request(self.start_url, callback=self.parse, dont_filter=True)

    def parse(self, response: Response):
        data = json.loads(response.text)
        courses = data.get("courses", None)
        for course in courses :
            item = UdacityItem()
            item["title"] = course.get("title", None)
            instructor = course.get("instructors", None)
            item["instructors"] = find_teachers(instructor)
            item["level"] = course.get("level", None)
            item["description"] = (course.get("summary" , '-'))
            item["prerequisites"] = course.get("required_knowledge", None)
            slug = course.get("slug")
            course_url = "https://cn.udacity.com/course/{}".format(slug)
            yield Request(course_url, callback=self.parse_details, dont_filter=True, meta={'item': item})

    def parse_details(self, response: Response):
        item = response.meta.get("item", UdacityItem())
        item["price"] = response.xpath(
            '//div[@class="section"]/div[1]/div/h5//text()').extract()
        item['source'] = 'udacity'
        yield item
        print("------------------------------------------------------------------------")



def find_teachers(a):
    b = []
    if a:
        for i in range(len(a)):
            b.append(a[i].get("name", None))
        return b
    else:
        return None
